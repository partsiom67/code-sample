from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
)

from app.domains.item import Item
from app.adapters.engines import models
from app.core.config import settings
from app.core.exceptions import (
    InvalidIdException,
    ItemNotFoundException,
    DatabaseConnectionException,
)
from app.ports.repositories.item_repository import ItemRepository


class MongoDBItemRepository(ItemRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db.get_collection("items")

    def convert_id(self, object_id: str) -> ObjectId:
        try:
            object_id = ObjectId(object_id)
            return object_id
        except InvalidId:
            raise InvalidIdException()

    async def get_items(self):
        try:
            limit = settings.ITEMS_LIMIT
            items = await self.collection.aggregate(
                [
                    {
                        "$group": {
                            "_id": "$source",
                            "items": {
                                "$topN": {
                                    "n": limit,
                                    "sortBy": {"created_at": -1},
                                    "output": "$$ROOT",
                                }
                            },
                        }
                    },
                    {"$unwind": "$items"},
                    {"$replaceWith": "$items"},
                ]
            ).to_list(length=None)
            return [
                Item.from_db_model(models.Item.model_validate(item)) for item in items
            ]
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def get_items_from_subscribed_topics(self, topics: list[str]):
        try:
            items = await self.collection.aggregate(
                [
                    {"$match": {"topic": {"$in": topics}}},
                    {
                        "$group": {
                            "_id": "$topic",
                            "date_of_appearance": {"$min": "$created_at"},
                            "items": {
                                "$push": {"item": "$$ROOT", "created_at": "$created_at"}
                            },
                        }
                    },
                    {"$sort": {"date_of_appearance": 1}},
                    {
                        "$project": {
                            "items": {
                                "$sortArray": {
                                    "input": "$items",
                                    "sortBy": {"created_at": -1},
                                }
                            }
                        }
                    },
                    {"$unwind": "$items"},
                    {"$replaceWith": "$items.item"},
                ]
            ).to_list(length=None)
            return [
                Item.from_db_model(models.Item.model_validate(item)) for item in items
            ]
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def create_item(self, item: Item):
        try:
            item_filter = {"unique_hash": item.unique_hash}
            new_item = models.Item(
                topic=item.topic,
                source=item.source,
                content=item.content,
                image=item.image,
                unique_hash=item.unique_hash,
                created_at=item.created_at,
            )
            result = await self.collection.update_one(
                filter=item_filter,
                update={
                    "$setOnInsert": new_item.model_dump(by_alias=True, exclude=["id"])
                },
                upsert=True,
            )
            if result.upserted_id:
                find_filter = {"_id": result.upserted_id}
            else:
                find_filter = item_filter
            item = await self.collection.find_one(find_filter)
            return Item.from_db_model(models.Item.model_validate(item))

        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def create_many_items(self, items: list[Item]):
        try:
            operations = [
                UpdateOne(
                    filter={"unique_hash": item.unique_hash},
                    update={
                        "$setOnInsert": models.Item(
                            topic=item.topic,
                            source=item.source,
                            content=item.content,
                            image=item.image,
                            unique_hash=item.unique_hash,
                            created_at=item.created_at,
                        ).model_dump(by_alias=True, exclude=["id"])
                    },
                    upsert=True,
                )
                for item in items
            ]
            await self.collection.bulk_write(operations)
            affected_items = await self.collection.find(
                {"$or": [{"unique_hash": item.unique_hash} for item in items]}
            ).to_list(length=None)
            return [
                Item.from_db_model(models.Item.model_validate(item))
                for item in affected_items
            ]
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def delete_item(self, item_id: str):
        try:
            item_id = self.convert_id(item_id)
            item = await self.collection.find_one({"_id": item_id})
            if not item:
                raise ItemNotFoundException()
            delete_result = await self.collection.delete_one({"_id": item_id})
            if delete_result.deleted_count == 1:
                return {"message": "Item deleted"}
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def delete_many_items(self, item_ids: list[str]):
        try:
            item_ids = [self.convert_id(item_id) for item_id in item_ids]

            count = await self.collection.count_documents({"_id": {"$in": item_ids}})
            if count != len(item_ids):
                raise ItemNotFoundException()

            delete_result = await self.collection.delete_many({"_id": {"$in": item_ids}})

            if delete_result.deleted_count == len(item_ids):
                return {"message": "Items deleted"}

        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def delete_old_items(self):
        try:
            limit = settings.ITEMS_LIMIT
            sources = [source["name"] for source in settings.SOURCES]

            item_groups = await self.collection.aggregate(
                [
                    {"$match": {"source": {"$in": sources}}},
                    {
                        "$group": {
                            "_id": "$source",
                            "ids": {
                                "$topN": {
                                    "n": limit,
                                    "sortBy": {"created_at": -1},
                                    "output": "$_id",
                                }
                            },
                        }
                    },
                ]
            ).to_list(length=None)

            delete_conditions = [
                {"source": group["_id"], "_id": {"$nin": group["ids"]}}
                for group in item_groups
                if group["ids"]
            ]
            if delete_conditions:
                await self.collection.delete_many({"$or": delete_conditions})
            return {"message": "Old items deleted"}
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

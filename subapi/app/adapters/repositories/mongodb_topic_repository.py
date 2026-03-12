from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
)

from app.domains.topic import Topic
from app.adapters.engines import models
from app.core.exceptions import (
    InvalidIdException,
    TopicNotFoundException,
    TopicAlreadyExistsException,
    DatabaseConnectionException,
)
from app.ports.repositories.topic_repository import TopicRepository


class MongoDBTopicRepository(TopicRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db.get_collection("topics")

    def convert_id(self, object_id: str) -> ObjectId:
        try:
            object_id = ObjectId(object_id)
            return object_id
        except InvalidId:
            raise InvalidIdException()

    async def get_topics(self):
        try:
            topics = await self.collection.find().to_list(length=None)
            return [
                Topic.from_db_model(models.Topic.model_validate(topic))
                for topic in topics
            ]
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def get_topic_by_id(self, topic_id: str):
        try:
            topic_id = self.convert_id(topic_id)
            topic = await self.collection.find_one({"_id": topic_id})
            if not topic:
                raise TopicNotFoundException()
            return Topic.from_db_model(models.Topic.model_validate(topic))
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def get_topic_by_name(self, topic_name: str):
        try:
            topic = await self.collection.find_one({"name": topic_name})
            if not topic:
                raise TopicNotFoundException()
            return Topic.from_db_model(models.Topic.model_validate(topic))
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def create_topic(self, topic: Topic):
        try:
            new_topic = models.Topic(name=topic.name)
            existing_topic = await self.collection.find_one({"name": topic.name})
            if existing_topic:
                raise TopicAlreadyExistsException()
            create_topic = await self.collection.insert_one(
                new_topic.model_dump(by_alias=True, exclude=["id"])
            )
            created_topic = await self.collection.find_one(
                {"_id": create_topic.inserted_id}
            )
            return Topic.from_db_model(models.Topic.model_validate(created_topic))

        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def delete_topic(self, topic_name: str):
        try:
            topic = await self.collection.find_one({"name": topic_name})
            if not topic:
                raise TopicNotFoundException()
            delete_result = await self.collection.delete_one({"name": topic_name})
            if delete_result.deleted_count == 1:
                return {"message": "Topic deleted"}
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

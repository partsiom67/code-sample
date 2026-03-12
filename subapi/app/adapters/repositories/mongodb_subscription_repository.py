from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
)

from app.domains.subscription import Subscription
from app.adapters.engines import models
from app.core.exceptions import (
    InvalidIdException,
    SubscriptionNotFoundException,
    SubscriptionAlreadyExistsException,
    DatabaseConnectionException,
)
from app.ports.repositories.subscription_repository import SubscriptionRepository


class MongoDBSubscriptionRepository(SubscriptionRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db.get_collection("subscriptions")

    def convert_id(self, object_id: str) -> ObjectId:
        try:
            object_id = ObjectId(object_id)
            return object_id
        except InvalidId:
            raise InvalidIdException()

    async def get_user_subscriptions(self, user_id: str):
        try:
            subscriptions = await self.collection.find({"user_id": user_id}).to_list(
                length=None
            )
            return [
                Subscription.from_db_model(
                    models.Subscription.model_validate(subscription)
                )
                for subscription in subscriptions
            ]
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def get_subscription_by_id(self, subscription_id: str, user_id: str):
        try:
            subscription_id = self.convert_id(subscription_id)
            subscription = await self.collection.find_one(
                {"_id": subscription_id, "user_id": user_id}
            )
            if not subscription:
                raise SubscriptionNotFoundException()
            return Subscription.from_db_model(
                models.Subscription.model_validate(subscription)
            )
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def create_subscription(self, subscription: Subscription, user_id: str):
        try:
            new_subscription = models.Subscription(
                user_id=user_id, topic=subscription.topic
            )
            existing_subscription = await self.collection.find_one(
                {"user_id": user_id, "topic": subscription.topic}
            )
            if existing_subscription:
                raise SubscriptionAlreadyExistsException()
            create_subscription = await self.collection.insert_one(
                new_subscription.model_dump(by_alias=True, exclude=["id"])
            )
            created_subscription = await self.collection.find_one(
                {"_id": create_subscription.inserted_id}
            )
            return Subscription.from_db_model(
                models.Subscription.model_validate(created_subscription)
            )

        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def delete_subscription(self, topic_name: str, user_id: str):
        try:
            subscription = await self.collection.find_one(
                {"topic": topic_name, "user_id": user_id}
            )
            if not subscription:
                raise SubscriptionNotFoundException()
            delete_result = await self.collection.delete_one(
                {"topic": topic_name, "user_id": user_id}
            )
            if delete_result.deleted_count == 1:
                return {"message": "Subscription deleted"}
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

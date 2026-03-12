from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
)

from app.domains.user import User
from app.utils.hashing import Hasher
from app.adapters.engines import models
from app.core.exceptions import (
    DatabaseConnectionException,
    InvalidIdException,
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.ports.repositories.user_repository import UserRepository


class MongoDBUserRepository(UserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db.get_collection("users")

    def convert_id(self, object_id: str) -> ObjectId:
        try:
            object_id = ObjectId(object_id)
            return object_id
        except InvalidId:
            raise InvalidIdException()

    async def get_user_by_id(self, user_id):
        try:
            user_id = self.convert_id(user_id)
            user = await self.collection.find_one({"_id": user_id})
            if not user:
                raise UserNotFoundException()
            return User.from_db_model(models.User.model_validate(user))
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def get_user_by_email(self, email):
        try:
            user = await self.collection.find_one({"email": email})
            if not user:
                raise UserNotFoundException()
            return User.from_db_model(models.User.model_validate(user))
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def create_user(self, user: User, password):
        try:
            new_user = models.User(
                username=user.username,
                email=user.email,
                hashed_password=Hasher.get_password_hash(password),
            )
            existing_user = await self.collection.find_one({"email": new_user.email})
            if existing_user:
                raise UserAlreadyExistsException()
            create_user = await self.collection.insert_one(
                new_user.model_dump(by_alias=True, exclude=["id"])
            )
            created_user = await self.collection.find_one(
                {"_id": create_user.inserted_id}
            )
            return User.from_db_model(models.User.model_validate(created_user))

        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

    async def delete_user(self, user_id):
        try:
            user_id = self.convert_id(user_id)
            user = await self.collection.find_one({"_id": user_id})
            if not user:
                raise UserNotFoundException()
            delete_result = await self.collection.delete_one({"_id": user_id})
            if delete_result.deleted_count == 1:
                return {"message": "User deleted"}
        except (ConnectionFailure, OperationFailure) as e:
            raise DatabaseConnectionException(e)

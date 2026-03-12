from bson import ObjectId

from app.domains.user import User
from app.utils.hashing import Hasher
from app.core.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.ports.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self, data={}):
        self.data = data

    async def get_user_by_id(self, user_id):
        user_memory = self.data.get(user_id, None)
        if user_memory is None:
            raise UserNotFoundException()
        return User(
            id=user_memory.id,
            email=user_memory.email,
            username=user_memory.username,
            hashed_password=user_memory.hashed_password,
        )

    async def get_user_by_email(self, email):
        user_memory = self.data.get(email, None)
        if user_memory is None:
            raise UserNotFoundException()
        return User(
            id=user_memory.id,
            email=user_memory.email,
            username=user_memory.username,
            hashed_password=user_memory.hashed_password,
        )

    async def create_user(self, user: User, password):
        new_user = User(
            id=str(ObjectId()),
            email=user.email,
            username=user.username,
            hashed_password=Hasher.get_password_hash(password),
        )
        user_memory = self.data.get(new_user.email, None)
        if user_memory:
            raise UserAlreadyExistsException()
        self.data[new_user.email] = new_user
        return new_user

    async def delete_user(self, user_id):
        user_memory = self.data.get(user_id, None)
        if user_memory is None:
            raise UserNotFoundException()
        return self.data.pop(user_id)

from abc import ABC, abstractmethod
from pydantic import EmailStr

from app.domains.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User, password: str) -> str:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> User:
        pass

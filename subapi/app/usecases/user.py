from pydantic import EmailStr

from app.domains.user import User
from app.ports.repositories.user_repository import UserRepository


class UserActionsUsecase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> User:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: EmailStr) -> User:
        return await self.user_repository.get_user_by_email(email)

    async def create_user(self, user: User, password: str) -> User:
        return await self.user_repository.create_user(user, password)

    async def delete_user(self, user_id: str) -> User:
        return await self.user_repository.delete_user(user_id)

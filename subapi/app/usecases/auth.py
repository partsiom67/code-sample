from datetime import datetime, timezone, timedelta
import jwt
from pydantic import EmailStr

from app.core.config import settings
from app.domains.user import User
from app.utils.hashing import Hasher
from app.core.exceptions import (
    UserUnauthorizedException,
    TokenExpiredSignatureException,
    TokenInvalidSignatureException,
)
from app.ports.repositories.user_repository import UserRepository


class AuthUsecase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def create_token(self, data: dict, expiration: timedelta) -> str:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + expiration
        payload.update({"exp": expire})
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    async def login(self, email: EmailStr, password: str) -> User:
        user = await self.user_repository.get_user_by_email(email)
        if not Hasher.verify_password(password, user.hashed_password):
            raise UserUnauthorizedException()
        subject = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }
        user.access_token = self.create_token(subject, settings.ACCESS_TOKEN_LIFETIME)
        user.refresh_token = self.create_token(subject, settings.REFRESH_TOKEN_LIFETIME)
        return user

    async def refresh_token(self, refresh_token: str) -> User:
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            user = await self.user_repository.get_user_by_email(payload["email"])
            user.access_token = self.create_token(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                settings.ACCESS_TOKEN_LIFETIME,
            )
            return user
        except jwt.ExpiredSignatureError:
            raise TokenExpiredSignatureException()
        except (
            KeyError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
            jwt.InvalidSignatureError,
        ):
            raise TokenInvalidSignatureException()

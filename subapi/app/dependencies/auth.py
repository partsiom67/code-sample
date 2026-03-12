import jwt

from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.dependencies.database import get_db
from app.adapters.repositories.mongodb_user_repository import MongoDBUserRepository

from app.core.exceptions import (
    UserNotFoundException,
    UserUnauthorizedException,
    TokenExpiredSignatureException,
    TokenInvalidSignatureException,
)


class JWTAuthDependency(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or credentials.scheme.lower() != "bearer":
            raise UserUnauthorizedException()

        try:
            payload = jwt.decode(
                credentials.credentials,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            user_id = payload.get("user_id")

            if not user_id:
                raise TokenInvalidSignatureException()

            return user_id

        except jwt.ExpiredSignatureError:
            raise TokenExpiredSignatureException()

        except (
            jwt.DecodeError,
            jwt.InvalidTokenError,
            jwt.InvalidSignatureError,
        ):
            raise TokenInvalidSignatureException()


async def get_auth_user(
    db=Depends(get_db),
    user_id: str = Depends(JWTAuthDependency()),
):
    try:
        repository = MongoDBUserRepository(db)
        user = await repository.get_user_by_id(user_id)
        return user

    except UserNotFoundException:
        raise UserUnauthorizedException()
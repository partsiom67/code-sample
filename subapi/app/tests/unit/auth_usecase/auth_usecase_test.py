from bson import ObjectId
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock
import pytest

from app.domains.user import User
from app.core.config import settings
from app.utils.hashing import Hasher
from app.core.exceptions import (
    UserNotFoundException,
    UserUnauthorizedException,
    TokenExpiredSignatureException,
    TokenInvalidSignatureException,
)
from app.adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from app.usecases.auth import AuthUsecase


@pytest.fixture()
def test_user():
    test_user = User(
        id=str(ObjectId()),
        email="testuser@email.com",
        username="testuser",
        hashed_password=Hasher.get_password_hash("testing"),
    )
    return test_user


@pytest.fixture()
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture()
def auth_usecase(user_repository):
    return AuthUsecase(user_repository)


@pytest.fixture()
def mock_time():
    def set_time(offset: timedelta):
        mock_time = datetime.now(timezone.utc) - offset
        mock = MagicMock()
        mock.now = MagicMock(return_value=mock_time)
        return mock

    return set_time


@pytest.mark.asyncio
async def test_login_success(user_repository, auth_usecase, test_user):
    user_repository.data = {test_user.email: test_user}
    user = await auth_usecase.login(test_user.email, "testing")
    assert user.access_token is not None
    assert user.refresh_token is not None


@pytest.mark.asyncio
async def test_login_user_not_found(user_repository, auth_usecase, test_user):
    user_repository.data = {test_user.email: test_user}
    with pytest.raises(UserNotFoundException):
        await auth_usecase.login("invalid@email.com", "testing")


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(user_repository, auth_usecase, test_user):
    user_repository.data = {test_user.email: test_user}
    with pytest.raises(UserUnauthorizedException):
        await auth_usecase.login(test_user.email, "invalid")


@pytest.mark.asyncio
async def test_refresh_success(user_repository, auth_usecase, test_user):
    user_repository.data = {test_user.email: test_user}
    token = auth_usecase.create_token(
        {
            "user_id": test_user.id,
            "username": test_user.username,
            "email": test_user.email,
        },
        settings.REFRESH_TOKEN_LIFETIME,
    )
    access_token = await auth_usecase.refresh_token(token)
    assert access_token is not None


@pytest.mark.asyncio
async def test_refresh_invalid_signature(user_repository, auth_usecase):
    with pytest.raises(TokenInvalidSignatureException):
        token = "invalid"
        await auth_usecase.refresh_token(token)


@pytest.mark.asyncio
async def test_refresh_expired_signature(
    user_repository, auth_usecase, test_user, mock_time, monkeypatch
):
    user_repository.data = {test_user.email: test_user}
    monkeypatch.setattr(
        "app.usecases.auth.datetime",
        mock_time(settings.ACCESS_TOKEN_LIFETIME + timedelta(days=1)),
    )
    with pytest.raises(TokenExpiredSignatureException):
        token = auth_usecase.create_token(
            {
                "user_id": test_user.id,
                "username": test_user.username,
                "email": test_user.email,
            },
            settings.ACCESS_TOKEN_LIFETIME,
        )
        monkeypatch.setattr(
            "app.usecases.auth.datetime",
            mock_time(settings.ACCESS_TOKEN_LIFETIME - timedelta(days=1)),
        )
        await auth_usecase.refresh_token(token)

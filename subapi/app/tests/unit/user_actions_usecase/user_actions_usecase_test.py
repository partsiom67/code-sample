from bson import ObjectId

import pytest

from app.domains.user import User
from app.utils.hashing import Hasher
from app.core.exceptions import UserNotFoundException, UserAlreadyExistsException
from app.adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from app.usecases.user import UserActionsUsecase


@pytest.fixture()
def test_user():
    test_user = User(
        id=ObjectId(),
        email="testuser@email.com",
        username="testuser",
        hashed_password=Hasher.get_password_hash("testing"),
    )
    return test_user


@pytest.fixture()
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture()
def user_actions_usecase(user_repository):
    return UserActionsUsecase(user_repository)


@pytest.mark.asyncio
async def test_create_user_success(user_repository, user_actions_usecase, test_user):
    new_user = User(email=test_user.email, username=test_user.username)
    user = await user_actions_usecase.create_user(new_user, "testing")
    assert user.username is not None


@pytest.mark.asyncio
async def test_create_user_already_exists(
    user_repository, user_actions_usecase, test_user
):
    user_repository.data = {test_user.email: test_user}
    with pytest.raises(UserAlreadyExistsException):
        new_user = User(
            email=test_user.email,
            username=test_user.username,
        )
        await user_actions_usecase.create_user(new_user, "testing")


@pytest.mark.asyncio
async def test_get_user_by_id_success(user_repository, user_actions_usecase, test_user):
    user_repository.data = {test_user.id: test_user}
    user = await user_actions_usecase.get_user_by_id(test_user.id)
    assert user.username is not None


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(
    user_repository, user_actions_usecase, test_user
):
    with pytest.raises(UserNotFoundException):
        await user_actions_usecase.get_user_by_id(test_user.id)


@pytest.mark.asyncio
async def test_get_user_by_email_success(
    user_repository, user_actions_usecase, test_user
):
    user_repository.data = {test_user.email: test_user}
    user = await user_actions_usecase.get_user_by_email(test_user.email)
    assert user.username is not None


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(
    user_repository, user_actions_usecase, test_user
):
    user_repository.data = {}
    with pytest.raises(UserNotFoundException):
        await user_actions_usecase.get_user_by_email(test_user.email)


@pytest.mark.asyncio
async def test_delete_user_success(user_repository, user_actions_usecase, test_user):
    user_repository.data = {test_user.id: test_user}
    await user_actions_usecase.delete_user(test_user.id)
    assert user_repository.data.get(test_user.id) is None


@pytest.mark.asyncio
async def test_delete_user_not_found(user_repository, user_actions_usecase, test_user):
    with pytest.raises(UserNotFoundException):
        await user_actions_usecase.delete_user(test_user.id)

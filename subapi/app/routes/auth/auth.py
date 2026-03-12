from fastapi import APIRouter, Depends

from .controllers import (
    UserCreate,
    UserCreated,
    UserLogin,
    UserLogged,
    AccessToken,
    RefreshToken,
)
from app.domains.user import User
from app.usecases.auth import AuthUsecase
from app.usecases.user import UserActionsUsecase
from app.dependencies.auth import get_auth_user
from app.dependencies.usecase import get_auth_usecase
from app.dependencies.usecase import get_user_actions_usecase


router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserCreated)
async def signup(
    data: UserCreate,
    auth_usecase: UserActionsUsecase = Depends(get_user_actions_usecase),
):
    return await auth_usecase.create_user(data.to_entity(), data.password)


@router.post("/login", response_model=UserLogged)
async def login(data: UserLogin, auth_usecase: AuthUsecase = Depends(get_auth_usecase)):
    return await auth_usecase.login(data.email, data.password)


@router.post("/refresh_token", response_model=AccessToken)
async def refresh_token(
    data: RefreshToken,
    auth_usecase: AuthUsecase = Depends(get_auth_usecase),
):
    return await auth_usecase.refresh_token(data.refresh_token)

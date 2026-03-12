from fastapi import APIRouter, Depends

from app.domains.user import User
from app.usecases.user import UserActionsUsecase

from app.dependencies.auth import get_auth_user
from app.dependencies.usecase import get_user_actions_usecase


router = APIRouter(prefix="/user")


@router.delete("/")
async def delete_user(
    user: User = Depends(get_auth_user),
    user_usecase: UserActionsUsecase = Depends(get_user_actions_usecase),
):
    return await user_usecase.delete_user(user.id)

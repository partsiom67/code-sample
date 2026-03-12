from typing import List
from fastapi import APIRouter, Depends

from .controllers import ItemSchema
from app.domains.user import User
from app.usecases.item import ItemActionsUsecase
from app.dependencies.auth import get_auth_user
from app.dependencies.usecase import get_item_actions_usecase


router = APIRouter(prefix="/item")


@router.get("/", response_model=List[ItemSchema])
async def get_items(
    user: User = Depends(get_auth_user),
    item_usecase: ItemActionsUsecase = Depends(get_item_actions_usecase),
):
    return await item_usecase.get_items()


@router.get("/subscribed/", response_model=List[ItemSchema])
async def get_items_from_subscribed_topics(
    user: User = Depends(get_auth_user),
    item_usecase: ItemActionsUsecase = Depends(get_item_actions_usecase),
):
    return await item_usecase.get_items_from_subscribed_topics(user.id)

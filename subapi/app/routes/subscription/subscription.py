from typing import List
from fastapi import APIRouter, Depends

from .controllers import (
    SubscriptionSchema,
    SubscriptionCreateSchema,
)
from app.domains.user import User
from app.usecases.subscription import SubscriptionActionsUsecase
from app.dependencies.auth import get_auth_user
from app.dependencies.usecase import get_subscription_actions_usecase


router = APIRouter(prefix="/subscription")


@router.get("/", response_model=List[SubscriptionSchema])
async def get_user_subscriptions(
    user: User = Depends(get_auth_user),
    subscription_usecase: SubscriptionActionsUsecase = Depends(
        get_subscription_actions_usecase
    ),
):
    return await subscription_usecase.get_user_subscriptions(user.id)


@router.post("/", response_model=SubscriptionSchema)
async def create_subscription(
    data: SubscriptionCreateSchema,
    user: User = Depends(get_auth_user),
    subscription_usecase: SubscriptionActionsUsecase = Depends(
        get_subscription_actions_usecase
    ),
):
    return await subscription_usecase.create_subscription(data.to_entity(), user.id)


@router.delete("/{topic_name}")
async def delete_subscription(
    topic_name: str,
    user: User = Depends(get_auth_user),
    subscription_usecase: SubscriptionActionsUsecase = Depends(
        get_subscription_actions_usecase
    ),
):
    return await subscription_usecase.delete_subscription(topic_name, user.id)

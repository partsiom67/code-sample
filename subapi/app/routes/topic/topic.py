from typing import List
from fastapi import APIRouter, Depends

from .controllers import TopicSchema, TopicCreateSchema
from app.domains.user import User
from app.usecases.topic import TopicActionsUsecase
from app.dependencies.auth import get_auth_user
from app.dependencies.usecase import get_topic_actions_usecase


router = APIRouter(prefix="/topic")


@router.get("/", response_model=List[TopicSchema])
async def get_topics(
    user: User = Depends(get_auth_user),
    topic_usecase: TopicActionsUsecase = Depends(get_topic_actions_usecase),
):
    return await topic_usecase.get_topics()


@router.post("/", response_model=TopicSchema)
async def create_topic(
    data: TopicCreateSchema,
    user: User = Depends(get_auth_user),
    topic_usecase: TopicActionsUsecase = Depends(get_topic_actions_usecase),
):
    return await topic_usecase.create_topic(data.to_entity())


@router.delete("/{topic_name}")
async def delete_topic(
    topic_name: str,
    user: User = Depends(get_auth_user),
    topic_usecase: TopicActionsUsecase = Depends(get_topic_actions_usecase),
):
    return await topic_usecase.delete_topic(topic_name)

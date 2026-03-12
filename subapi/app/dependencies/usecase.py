from fastapi import Depends

from app.dependencies.database import get_db

from app.usecases.auth import AuthUsecase
from app.usecases.user import UserActionsUsecase
from app.usecases.subscription import SubscriptionActionsUsecase
from app.usecases.topic import TopicActionsUsecase
from app.usecases.item import ItemActionsUsecase
from app.usecases.webhook import WebhookUsecase
from app.adapters.repositories.mongodb_user_repository import (
    MongoDBUserRepository,
)
from app.adapters.repositories.mongodb_subscription_repository import (
    MongoDBSubscriptionRepository,
)
from app.adapters.repositories.mongodb_topic_repository import (
    MongoDBTopicRepository,
)
from app.adapters.repositories.mongodb_item_repository import (
    MongoDBItemRepository,
)
from app.dependencies.service import get_source_service


def get_auth_usecase(db=Depends(get_db)):
    return AuthUsecase(MongoDBUserRepository(db))


def get_user_actions_usecase(db=Depends(get_db)):
    return UserActionsUsecase(MongoDBUserRepository(db))


def get_subscription_actions_usecase(db=Depends(get_db)):
    return SubscriptionActionsUsecase(MongoDBSubscriptionRepository(db))


def get_topic_actions_usecase(db=Depends(get_db)):
    return TopicActionsUsecase(MongoDBTopicRepository(db))


def get_item_actions_usecase(
    db=Depends(get_db), source_service=Depends(get_source_service)
):
    return ItemActionsUsecase(
        source_service, MongoDBItemRepository(db), MongoDBSubscriptionRepository(db)
    )


def get_webhook_usecase(db=Depends(get_db)):
    return WebhookUsecase(MongoDBItemRepository(db))

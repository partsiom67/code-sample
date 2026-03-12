import pytest
from bson import ObjectId
from datetime import datetime
from unittest.mock import AsyncMock
import mongomock_motor

from app.domains.item import Item
from app.domains.subscription import Subscription
from app.usecases.item import ItemActionsUsecase
from app.services.source_service import SourceService
from app.adapters.repositories.mongodb_item_repository import MongoDBItemRepository
from app.ports.repositories.subscription_repository import SubscriptionRepository


@pytest.fixture(scope="function")
def mongo_client():
    return mongomock_motor.AsyncMongoMockClient()


@pytest.fixture(scope="function")
def mock_db(mongo_client):
    return mongo_client["test_db"]


@pytest.fixture(scope="function")
def item_repository(mock_db):
    return MongoDBItemRepository(mock_db)


@pytest.fixture(scope="function")
def source_service():
    mock_service = AsyncMock(spec=SourceService)
    mock_service.get_from_sources.return_value = {
        "test_source": [
            {
                "topic": "test_topic",
                "data": "test_content",
                "image": "test_image",
                "created_at": datetime.now(),
            }
        ]
    }
    return mock_service


@pytest.fixture(scope="function")
def subscription_repository():
    mock_repository = AsyncMock(spec=SubscriptionRepository)
    mock_repository.get_user_subscriptions.return_value = [
        Subscription(id=str(ObjectId()), user_id="test_user_id", topic="test_topic")
    ]
    return mock_repository


@pytest.fixture(scope="function")
def item_actions_usecase(source_service, item_repository, subscription_repository):
    return ItemActionsUsecase(
        source_service=source_service,
        item_repository=item_repository,
        subscription_repository=subscription_repository,
    )


@pytest.fixture(scope="function")
def test_item():
    return Item(
        id=str(ObjectId()),
        topic="test_topic",
        source="test_source",
        content="test_content",
        image="test_image",
        unique_hash="test_unique_hash",
        created_at=datetime.now(),
    )


@pytest.mark.asyncio
async def test_create_item(item_actions_usecase, item_repository, test_item):
    result = await item_actions_usecase.create_item(test_item)

    assert result.topic == test_item.topic
    assert result.content == test_item.content

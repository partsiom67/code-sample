from app.domains.item import Item
from app.core.config import settings
from app.services.source_service import SourceService
from app.ports.repositories.item_repository import ItemRepository
from app.ports.repositories.subscription_repository import SubscriptionRepository


class ItemActionsUsecase:
    def __init__(
        self,
        source_service: SourceService,
        item_repository: ItemRepository,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self.source_service = source_service
        self.item_repository = item_repository
        self.subscription_repository = subscription_repository

    async def _fetch_sources(self) -> None:
        sources = settings.SOURCES
        responses = await self.source_service.get_from_sources(sources)
        items = [
            Item(
                topic=item.get("topic", None),
                source=source_name,
                content=item.get("data", None),
                image=item.get("image", None),
                created_at=item.get("created_at", None),
            )
            for source_name, items in responses.items()
            for item in items
        ]
        if items:
            await self.item_repository.create_many_items(items)

    async def get_items(self) -> list[Item]:
        await self._fetch_sources()
        return await self.item_repository.get_items()

    async def get_items_from_subscribed_topics(self, user_id: str) -> list[Item]:
        await self._fetch_sources()
        subscriptions = await self.subscription_repository.get_user_subscriptions(
            user_id
        )
        subscribed_topics = [subscription.topic for subscription in subscriptions]
        return await self.item_repository.get_items_from_subscribed_topics(
            subscribed_topics
        )

    async def create_item(self, item: Item) -> Item:
        return await self.item_repository.create_item(item)

    async def create_many_items(self, items: list[Item]) -> list[Item]:
        return await self.item_repository.create_many_items(items)

    async def delete_item(self, item_id: str):
        return await self.item_repository.delete_item(item_id)

    async def delete_many_items(self, item_ids: list[str]):
        return await self.item_repository.delete_many_items(item_ids)

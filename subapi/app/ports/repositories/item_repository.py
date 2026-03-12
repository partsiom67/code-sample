from abc import ABC, abstractmethod

from app.domains.item import Item


class ItemRepository(ABC):
    @abstractmethod
    async def get_items(self) -> list[Item]:
        pass

    @abstractmethod
    async def get_items_from_subscribed_topics(self, topics: list[str]) -> list[Item]:
        pass

    @abstractmethod
    async def create_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    async def create_many_items(self, items: list[Item]) -> list[Item]:
        pass

    @abstractmethod
    async def delete_item(self, item_id: str):
        pass

    @abstractmethod
    async def delete_many_items(self, item_ids: list[str]):
        pass

    @abstractmethod
    async def delete_old_items(self):
        pass

from app.domains.item import Item
from app.ports.repositories.item_repository import ItemRepository


class WebhookUsecase:
    def __init__(
        self,
        item_repository: ItemRepository,
    ) -> None:
        self.item_repository = item_repository

    async def process_data(self, source_name, payload) -> None:
        item = Item(
            topic=payload.get("topic", None),
            source=source_name,
            content=payload.get("data", None),
            image=payload.get("image", None),
            created_at=payload.get("created_at", None),
        )
        await self.item_repository.create_item(item)

import logging
from app.adapters.engines.mongodb import get_database
from app.adapters.repositories.mongodb_item_repository import MongoDBItemRepository

logger = logging.getLogger(__name__)

class CleanupService:
    def __init__(self):
        self.db = get_database()
        self.item_repository = MongoDBItemRepository(self.db)

    async def cleanup_items(self):
        try:
            await self.item_repository.delete_old_items()
        except Exception:
            logger.exception("Cleanup job failed")
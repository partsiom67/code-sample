from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.adapters.engines.mongodb import get_database


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    db = get_database()
    yield db

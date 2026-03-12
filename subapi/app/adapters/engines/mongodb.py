from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings


@lru_cache
def get_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    return client


@lru_cache
def get_database() -> AsyncIOMotorDatabase:
    client = get_client()
    db = client.get_database(settings.DATABASE_NAME)
    return db

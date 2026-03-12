from typing import AsyncGenerator

from app.utils.api_client import APIClient


async def get_api_client() -> AsyncGenerator[APIClient, None]:
    async with APIClient() as client:
        yield client

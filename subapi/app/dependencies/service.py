from typing import AsyncGenerator
from fastapi import Depends
from app.utils.api_client import APIClient
from app.services.source_service import SourceService


async def get_api_client() -> AsyncGenerator[APIClient, None]:
    async with APIClient() as client:
        yield client


async def get_source_service(
    api_client: APIClient = Depends(get_api_client),
) -> SourceService:
    return SourceService(api_client)

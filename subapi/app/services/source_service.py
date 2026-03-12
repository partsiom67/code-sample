import asyncio
import logging
from typing import Dict, Any, List

from app.utils.api_client import APIClient
from app.core.settings import SourceType

logger = logging.getLogger(__name__)


class SourceService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def get_from_sources(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        responses: Dict[str, Any] = {}

        fetch_sources = [
            source for source in sources
            if source["type"] == SourceType.FETCH.value
        ]

        tasks = [self.api_client.get(source["url"]) for source in fetch_sources]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for source, result in zip(fetch_sources, results):

            if isinstance(result, Exception):
                logger.warning(
                    "Failed to fetch source '%s': %s",
                    source["name"],
                    str(result),
                )
                continue

            if result is not None:
                responses[source["name"]] = result

        return responses
import asyncio
import httpx

from typing import Optional, Dict, Any

from app.core.config import settings


class APIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(settings.TIMEOUT))
        self.max_retries = settings.MAX_RETRIES
        self.delay = settings.RETRY_DELAY

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def get(self, url: str) -> Optional[Dict[str, Any]]:
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.HTTPError) as e:
                if attempt < self.max_retries:
                    await asyncio.sleep(self.delay)
                    continue
                return None

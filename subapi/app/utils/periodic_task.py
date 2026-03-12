import asyncio
from typing import Optional


class PeriodicTask:
    def __init__(self):
        self.task: Optional[asyncio.Task] = None
        self.is_running = False

    async def run_periodic(self, func, interval_seconds: int):
        self.is_running = True
        while self.is_running:
            await func()
            await asyncio.sleep(interval_seconds)

    def start(self, func, interval_seconds: int):
        self.task = asyncio.create_task(self.run_periodic(func, interval_seconds))

    async def stop(self):
        if self.task:
            self.is_running = False
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

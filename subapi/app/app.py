from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from app.core.config import settings
    from app.utils.periodic_task import PeriodicTask
    from app.services.cleanup_service import CleanupService

    cleanup_task = PeriodicTask()
    cleanup_service = CleanupService()
    cleanup_task.start(cleanup_service.cleanup_items, settings.INTERVAL)

    yield

    # Shutdown
    await cleanup_task.stop()


app = FastAPI(lifespan=lifespan)

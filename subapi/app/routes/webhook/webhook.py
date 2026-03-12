import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.usecases.webhook import WebhookUsecase
from app.dependencies.usecase import get_webhook_usecase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook")


@router.post("/{source}")
async def webhook(
    source: str,
    request: Request,
    webhook_usecase: WebhookUsecase = Depends(get_webhook_usecase),
):
    try:
        payload = await request.json()
        return await webhook_usecase.process_data(source, payload)

    except RequestValidationError as e:
        logger.warning("Invalid webhook payload from %s: %s", source, e)

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "invalid payload"},
        )

    except Exception as e:
        logger.exception("Webhook processing failed for source: %s", source)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "internal server error"},
        )
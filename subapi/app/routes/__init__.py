from fastapi import APIRouter

from app.routes.auth import auth
from app.routes.user import user
from app.routes.subscription import subscription
from app.routes.topic import topic
from app.routes.item import item
from app.routes.webhook import webhook


router = APIRouter(prefix="/api")
router.include_router(auth.router, tags=["Auth"])
router.include_router(user.router, tags=["User"])
router.include_router(subscription.router, tags=["Subscription"])
router.include_router(topic.router, tags=["Topic"])
router.include_router(item.router, tags=["Item"])
router.include_router(webhook.router, tags=["Webhook"])

from typing import Optional
from pydantic import BaseModel

from app.domains.subscription import Subscription


class SubscriptionSchema(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    topic: Optional[str] = None


class SubscriptionCreateSchema(BaseModel):
    topic: str

    def to_entity(self):
        return Subscription(topic=self.topic)

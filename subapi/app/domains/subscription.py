from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Subscription:
    id: Optional[str] = None
    user_id: Optional[str] = None
    topic: Optional[str] = None
    created_at: Optional[datetime] = None

    def convert_to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def to_entity(cls, subscribtion):
        return Subscription(
            id=subscribtion.id,
            user_id=subscribtion.user_id,
            topic=subscribtion.topiс,
            created_at=subscribtion.created_at,
        )

    @classmethod
    def from_db_model(cls, subscription_model):
        return cls(
            id=subscription_model.id,
            user_id=subscription_model.user_id,
            topic=subscription_model.topic,
            created_at=subscription_model.created_at,
        )

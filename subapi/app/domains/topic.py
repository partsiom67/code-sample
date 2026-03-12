from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Topic:
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None

    def convert_to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def to_entity(cls, topic):
        return Topic(
            id=topic.id,
            name=topic.user_id,
            created_at=topic.created_at,
        )

    @classmethod
    def from_db_model(cls, topic_model):
        return cls(
            id=topic_model.id,
            name=topic_model.name,
            created_at=topic_model.created_at,
        )

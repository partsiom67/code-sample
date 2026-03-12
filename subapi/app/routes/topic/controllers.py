from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domains.topic import Topic


class TopicSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None


class TopicCreateSchema(BaseModel):
    name: str

    def to_entity(self):
        return Topic(name=self.name)

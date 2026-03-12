from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ItemSchema(BaseModel):
    id: Optional[str] = None
    topic: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    created_at: Optional[datetime] = None
    fetched_at: Optional[datetime] = None

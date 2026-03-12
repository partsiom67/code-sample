import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Item:
    id: Optional[str] = None
    topic: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    unique_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    fetched_at: Optional[datetime] = None

    def __post_init__(self):
        """Runs after initialization"""
        self.generate_hash()

    def generate_hash(self) -> None:
        """Generate a unique hash based on item content"""
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.isoformat()
        else:
            created_at_str = self.created_at
        hash_input = {
            "topic": self.topic if self.topic else "",
            "source": self.source if self.source else "",
            "content": self.content if self.content else "",
            "image": self.image if self.image else "",
            "created_at": created_at_str if created_at_str else "",
        }
        hash_string = json.dumps(hash_input, sort_keys=True)
        self.unique_hash = hashlib.md5(hash_string.encode()).hexdigest()

    def convert_to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def to_entity(cls, item):
        return Item(
            id=item.id,
            topic=item.topic,
            source=item.source,
            content=item.content,
            image=item.image,
            created_at=item.created_at,
            fetched_at=item.fetched_at,
        )

    @classmethod
    def from_db_model(cls, item_model):
        return cls(
            id=item_model.id,
            topic=item_model.topic,
            source=item_model.source,
            content=item_model.content,
            image=item_model.image,
            created_at=item_model.created_at,
            fetched_at=item_model.fetched_at,
        )

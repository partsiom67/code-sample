from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


@dataclass
class User:
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    def convert_to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def to_entity(cls, user):
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.password,
            created_at=user.created_at,
            modified_at=user.modified_at,
        )

    @classmethod
    def from_db_model(cls, user_model):
        return cls(
            id=user_model.id,
            email=user_model.email,
            username=user_model.username,
            hashed_password=user_model.hashed_password,
            created_at=user_model.created_at,
            modified_at=user_model.modified_at,
        )

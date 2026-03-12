from typing import Optional
from pydantic import BaseModel, EmailStr

from app.domains.user import User


class UserSchema(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    def to_entity(self):
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
        )

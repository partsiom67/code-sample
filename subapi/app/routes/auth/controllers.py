from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.domains.user import User


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    def to_entity(self):
        return User(username=self.username, email=self.email)


class UserCreated(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLogged(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class AccessToken(BaseModel):
    access_token: str

    class Config:
        from_attributes = True


class RefreshToken(BaseModel):
    refresh_token: str

# File: src/backend/app/models/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserProfile(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[int] = None



class UserInDB(UserProfile):
    hashed_password: str

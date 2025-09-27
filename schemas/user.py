from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class User(UserBase):
    id: int
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True

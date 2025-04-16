from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    userid: UUID
    created_at: datetime
    last_login: datetime | None

    class Config:
        from_attributes = True

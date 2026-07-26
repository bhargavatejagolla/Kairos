from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, EmailStr, Field

from app.schemas.base import SchemaBase


class UserCreate(SchemaBase):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(SchemaBase):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None


class UserResponse(SchemaBase):
    id: UUID
    email: EmailStr
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserPublic(UserResponse):
    pass


class UserLogin(SchemaBase):
    email: EmailStr
    password: str


class UserListResponse(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    users: list[UserResponse]

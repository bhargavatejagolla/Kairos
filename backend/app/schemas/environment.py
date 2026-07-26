from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import SchemaBase


class EnvironmentCreate(SchemaBase):
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    color: str | None = Field(None, max_length=20)
    description: str | None = Field(None, max_length=255)


class EnvironmentUpdate(SchemaBase):
    name: str | None = Field(None, max_length=50)
    color: str | None = Field(None, max_length=20)
    description: str | None = Field(None, max_length=255)


class EnvironmentResponse(SchemaBase):
    id: UUID
    name: str
    slug: str
    color: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

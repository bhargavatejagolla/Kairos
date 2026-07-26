from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import SchemaBase


class PermissionResponse(SchemaBase):
    id: UUID
    name: str
    description: str | None


class RoleCreate(SchemaBase):
    name: str = Field(
        min_length=2,
        max_length=50,
    )
    description: str | None = None


class RoleUpdate(SchemaBase):
    description: str | None = None


class RoleResponse(SchemaBase):
    id: UUID
    name: str
    description: str | None
    permissions: list[PermissionResponse]
    created_at: datetime
    updated_at: datetime


class AssignPermissionRequest(SchemaBase):
    permission_id: UUID

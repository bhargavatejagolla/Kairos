from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.core.organization import MembershipStatus, OrganizationStatus
from app.schemas.base import SchemaBase


class OrganizationCreate(SchemaBase):
    name: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)
    description: str | None = None
    website: str | None = None
    logo_url: str | None = None


class OrganizationUpdate(SchemaBase):
    name: str | None = Field(None, max_length=150)
    description: str | None = None
    website: str | None = None
    logo_url: str | None = None
    status: OrganizationStatus | None = None


class OrganizationResponse(SchemaBase):
    id: UUID
    name: str
    slug: str
    description: str | None
    website: str | None
    logo_url: str | None
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime


class AddMemberRequest(SchemaBase):
    user_id: UUID
    role_id: UUID


class ChangeMemberRoleRequest(SchemaBase):
    role_id: UUID


class MemberResponse(SchemaBase):
    id: UUID
    organization_id: UUID
    user_id: UUID
    role_id: UUID
    invited_by_id: UUID | None
    status: MembershipStatus
    joined_at: datetime
    created_at: datetime
    updated_at: datetime

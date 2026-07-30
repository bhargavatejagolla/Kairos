from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.enums import RuntimeType, ServiceStatus, ServiceTier, ServiceType


class ServiceCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    service_type: ServiceType = ServiceType.API
    runtime: RuntimeType = RuntimeType.UNKNOWN
    tier: ServiceTier = ServiceTier.TIER_3
    repository_url: str | None = None
    documentation_url: str | None = None
    dashboard_url: str | None = None
    owner_team: str | None = None

class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    service_type: ServiceType | None = None
    runtime: RuntimeType | None = None
    tier: ServiceTier | None = None
    status: ServiceStatus | None = None
    repository_url: str | None = None
    documentation_url: str | None = None
    dashboard_url: str | None = None
    owner_team: str | None = None

class ServiceResponse(ServiceCreate):
    id: UUID
    organization_id: UUID
    project_id: UUID
    environment_id: UUID
    status: ServiceStatus
    created_by_id: UUID | None
    updated_by_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

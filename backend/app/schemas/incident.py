from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.db.models.enums import IncidentStatus, IncidentSeverity, IncidentPriority, IncidentSource

class IncidentCreate(BaseModel):
    title: str
    description: str
    service_id: UUID
    severity: IncidentSeverity = IncidentSeverity.SEV_3
    priority: IncidentPriority = IncidentPriority.P3
    source: IncidentSource = IncidentSource.MANUAL

class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: IncidentStatus | None = None
    severity: IncidentSeverity | None = None
    priority: IncidentPriority | None = None

class IncidentResponse(BaseModel):
    id: UUID
    organization_id: UUID
    project_id: UUID
    service_id: UUID
    number: str
    title: str
    description: str | None
    status: IncidentStatus
    severity: IncidentSeverity
    priority: IncidentPriority
    source: IncidentSource
    detected_at: datetime | None
    started_at: datetime | None
    acknowledged_at: datetime | None
    mitigated_at: datetime | None
    resolved_at: datetime | None
    closed_at: datetime | None
    assigned_to: UUID | None
    created_by_id: UUID | None
    updated_by_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

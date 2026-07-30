from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.enums import AlertSeverity, AlertStatus


class AlertCreate(BaseModel):
    rule_id: UUID
    service_id: UUID
    incident_id: UUID | None = None
    severity: AlertSeverity
    title: str
    message: str | None = None
    fingerprint: str
    triggered_at: datetime

class AlertResponse(AlertCreate):
    id: UUID
    status: AlertStatus
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None
    closed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

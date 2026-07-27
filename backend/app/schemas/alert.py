from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.db.models.enums import AlertStatus, AlertSeverity

class AlertCreate(BaseModel):
    rule_id: UUID
    service_id: UUID
    incident_id: Optional[UUID] = None
    severity: AlertSeverity
    title: str
    message: Optional[str] = None
    fingerprint: str
    triggered_at: datetime

class AlertResponse(AlertCreate):
    id: UUID
    status: AlertStatus
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

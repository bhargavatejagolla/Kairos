from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import SchemaBase


class ProjectSettingsUpdate(SchemaBase):
    timezone: str | None = Field(None, max_length=50)
    retention_days: int | None = Field(None, ge=1, le=3650)
    ai_enabled: bool | None = None
    notifications_enabled: bool | None = None
    incident_auto_creation: bool | None = None
    default_severity: str | None = Field(None, max_length=20)
    alert_grouping: str | None = Field(None, max_length=50)
    tags: list[str] | None = None


class ProjectSettingsResponse(SchemaBase):
    id: UUID
    project_id: UUID
    timezone: str
    retention_days: int
    ai_enabled: bool
    notifications_enabled: bool
    incident_auto_creation: bool
    default_severity: str
    alert_grouping: str
    tags: list[str] | None
    created_at: datetime
    updated_at: datetime

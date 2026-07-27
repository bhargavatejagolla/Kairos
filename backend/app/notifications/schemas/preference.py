from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class NotificationPreferenceBase(BaseModel):
    incident_enabled: bool = True
    alert_enabled: bool = True
    security_enabled: bool = True
    system_enabled: bool = True
    weekly_reports: bool = True
    marketing_enabled: bool = False

class NotificationPreferenceUpdate(BaseModel):
    incident_enabled: bool | None = None
    alert_enabled: bool | None = None
    security_enabled: bool | None = None
    system_enabled: bool | None = None
    weekly_reports: bool | None = None
    marketing_enabled: bool | None = None

class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

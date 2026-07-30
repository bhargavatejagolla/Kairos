from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.notifications.enums.category import NotificationCategory
from app.notifications.enums.channel import NotificationChannel
from app.notifications.enums.priority import NotificationPriority
from app.notifications.enums.status import NotificationStatus


class NotificationBase(BaseModel):
    recipient_user_id: UUID | None = None
    event_type: str | None = None
    channel: NotificationChannel = NotificationChannel.EMAIL
    priority: NotificationPriority = NotificationPriority.NORMAL
    category: NotificationCategory = NotificationCategory.SYSTEM
    subject: str | None = None
    template_id: UUID | None = None
    payload: dict | None = None

class NotificationCreate(NotificationBase):
    organization_id: UUID
    project_id: UUID | None = None
    scheduled_at: datetime | None = None

class NotificationResponse(NotificationBase):
    id: UUID
    organization_id: UUID
    project_id: UUID | None
    status: NotificationStatus
    created_by: UUID | None
    scheduled_at: datetime | None
    sent_at: datetime | None
    failed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

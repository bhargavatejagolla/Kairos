from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.notifications.enums.category import NotificationCategory

class EmailTemplateBase(BaseModel):
    name: str
    category: NotificationCategory = NotificationCategory.SYSTEM
    subject_template: str
    html_template: str
    text_template: str | None = None
    is_active: bool = True

class EmailTemplateCreate(EmailTemplateBase):
    slug: str

class EmailTemplateUpdate(BaseModel):
    name: str | None = None
    category: NotificationCategory | None = None
    subject_template: str | None = None
    html_template: str | None = None
    text_template: str | None = None
    is_active: bool | None = None

class EmailTemplateResponse(EmailTemplateBase):
    id: UUID
    organization_id: UUID | None
    slug: str
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

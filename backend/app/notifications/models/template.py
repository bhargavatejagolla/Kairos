from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Boolean, Text

from app.db.models.base import BaseModel
from app.notifications.enums.category import NotificationCategory

class EmailTemplate(BaseModel):
    __tablename__ = "email_templates"

    organization_id: Mapped[UUID | None] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    category: Mapped[NotificationCategory] = mapped_column(default=NotificationCategory.SYSTEM)
    
    subject_template: Mapped[str] = mapped_column(String(500))
    html_template: Mapped[str] = mapped_column(Text)
    text_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    version: Mapped[int] = mapped_column(default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

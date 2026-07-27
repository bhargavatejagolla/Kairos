from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, JSON

from app.db.models.base import BaseModel
from app.notifications.enums.status import NotificationStatus
from app.notifications.enums.priority import NotificationPriority
from app.notifications.enums.channel import NotificationChannel
from app.notifications.enums.category import NotificationCategory

class Notification(BaseModel):
    __tablename__ = "notifications"

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[UUID | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    recipient_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    event_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    channel: Mapped[NotificationChannel] = mapped_column(default=NotificationChannel.EMAIL)
    status: Mapped[NotificationStatus] = mapped_column(default=NotificationStatus.PENDING)
    priority: Mapped[NotificationPriority] = mapped_column(default=NotificationPriority.NORMAL)
    category: Mapped[NotificationCategory] = mapped_column(default=NotificationCategory.SYSTEM)
    
    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    template_id: Mapped[UUID | None] = mapped_column(ForeignKey("email_templates.id", ondelete="SET NULL"), nullable=True)
    
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    deliveries = relationship("NotificationDelivery", back_populates="notification", cascade="all, delete-orphan")
    audits = relationship("NotificationAudit", back_populates="notification", cascade="all, delete-orphan")

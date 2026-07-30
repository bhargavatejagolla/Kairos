from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class NotificationAudit(BaseModel):
    __tablename__ = "notification_audits"

    notification_id: Mapped[UUID] = mapped_column(ForeignKey("notifications.id", ondelete="CASCADE"))
    action: Mapped[str] = mapped_column(String(100)) # e.g. Queued, Rendered, Sending, Delivered, Failed, Cancelled
    performed_by: Mapped[str | None] = mapped_column(String(255), nullable=True) # system, user_id, or worker_id
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    metadata_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    notification = relationship("Notification", back_populates="audits")

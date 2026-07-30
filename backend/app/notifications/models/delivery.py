from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class NotificationDelivery(BaseModel):
    __tablename__ = "notification_deliveries"

    notification_id: Mapped[UUID] = mapped_column(ForeignKey("notifications.id", ondelete="CASCADE"))
    attempt: Mapped[int] = mapped_column(default=1)
    provider: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(nullable=True)
    
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    notification = relationship("Notification", back_populates="deliveries")

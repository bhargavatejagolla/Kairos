from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Boolean

from app.db.models.base import BaseModel

class NotificationPreference(BaseModel):
    __tablename__ = "notification_preferences"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    
    incident_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    security_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    system_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    weekly_reports: Mapped[bool] = mapped_column(Boolean, default=True)
    marketing_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

import uuid

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ProjectSettings(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "project_settings"

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    retention_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    incident_auto_creation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default_severity: Mapped[str] = mapped_column(String(20), default="SEV-3", nullable=False)
    alert_grouping: Mapped[str] = mapped_column(String(50), default="time_based", nullable=False)
    tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    project = relationship("Project", back_populates="settings")

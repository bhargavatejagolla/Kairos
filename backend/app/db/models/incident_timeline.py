from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.enums import TimelineEvent
from app.db.models.mixins import UUIDPrimaryKeyMixin


class IncidentTimeline(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "incident_timeline"

    incident_id = Column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(Enum(TimelineEvent), nullable=False)
    actor_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message = Column(String)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_incident_timeline_created_at", "created_at"),
    )
    
    incident = relationship("Incident", backref="timeline_events")
    actor = relationship("User", foreign_keys=[actor_id])

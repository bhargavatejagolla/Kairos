from uuid import UUID
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Enum, DateTime, Index
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin
from app.db.models.enums import IncidentStatus, IncidentSeverity, IncidentPriority, IncidentSource

class Incident(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "incidents"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    
    number = Column(String(32), unique=True, index=True, nullable=False) # e.g. INC-000001
    title = Column(String(255), nullable=False)
    description = Column(String)
    
    status = Column(Enum(IncidentStatus), nullable=False, default=IncidentStatus.OPEN, index=True)
    severity = Column(Enum(IncidentSeverity), nullable=False, default=IncidentSeverity.SEV_3, index=True)
    priority = Column(Enum(IncidentPriority), nullable=False, default=IncidentPriority.P3, index=True)
    source = Column(Enum(IncidentSource), nullable=False, default=IncidentSource.MANUAL)
    
    detected_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    acknowledged_at = Column(DateTime(timezone=True))
    mitigated_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    
    assigned_to = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    __table_args__ = (
        Index("ix_incidents_created_at", "created_at"),
    )
    
    organization = relationship("Organization")
    project = relationship("Project")
    service = relationship("Service", backref="incidents")
    assignee = relationship("User", foreign_keys=[assigned_to])

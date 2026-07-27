from sqlalchemy import Column, String, ForeignKey, Enum, DateTime, Index
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin
from app.db.models.enums import AlertStatus, AlertSeverity

class Alert(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "alerts"

    rule_id = Column(ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    incident_id = Column(ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True, index=True)
    
    status = Column(Enum(AlertStatus), nullable=False, default=AlertStatus.OPEN, index=True)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    message = Column(String)
    
    fingerprint = Column(String(255), nullable=False, index=True)
    
    triggered_at = Column(DateTime(timezone=True), nullable=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    service = relationship("Service")
    incident = relationship("Incident")

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin

class MaintenanceWindow(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "maintenance_windows"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=True, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(String)
    
    recurrence = Column(String(255), nullable=True) # E.g., RRULE or simple cron
    
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String(50), nullable=False, default="UTC")
    
    organization = relationship("Organization")
    service = relationship("Service")

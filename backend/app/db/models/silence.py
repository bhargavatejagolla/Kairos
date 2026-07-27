from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin

class Silence(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "silences"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=True, index=True)
    
    matchers = Column(JSON, nullable=False) # E.g., {"severity": "WARNING", "env": "prod"}
    reason = Column(String, nullable=False)
    
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    
    organization = relationship("Organization")
    service = relationship("Service")

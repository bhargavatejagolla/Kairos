from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AlertGroup(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "alert_groups"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    root_alert_id = Column(ForeignKey("alerts.id", ondelete="SET NULL"), nullable=True)
    
    correlation_key = Column(String(255), nullable=False, index=True)
    
    status = Column(String(50), nullable=False, default="OPEN") # e.g. OPEN, CLOSED
    summary = Column(String)
    
    opened_at = Column(DateTime(timezone=True), nullable=False, index=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        UniqueConstraint("organization_id", "correlation_key", name="uix_org_correlation_key"),
    )
    
    organization = relationship("Organization")
    root_alert = relationship("Alert", foreign_keys=[root_alert_id])
    correlations = relationship("AlertCorrelation", backref="group", cascade="all, delete-orphan")

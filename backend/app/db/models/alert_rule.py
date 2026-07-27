from sqlalchemy import Column, String, ForeignKey, Enum, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin
from app.db.models.enums import RuleStatus, AlertSeverity

class AlertRule(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "alert_rules"

    service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(String)
    
    enabled = Column(Boolean, default=True, nullable=False, index=True)
    status = Column(Enum(RuleStatus), nullable=False, default=RuleStatus.ACTIVE)
    severity = Column(Enum(AlertSeverity), nullable=False, index=True)
    
    evaluation_window = Column(String(50), nullable=False, default="5m")
    cooldown = Column(String(50), nullable=False, default="15m")
    
    __table_args__ = (
        UniqueConstraint("service_id", "slug", name="uix_service_rule_slug"),
    )
    
    service = relationship("Service", backref="alert_rules")
    definitions = relationship("RuleDefinition", backref="alert_rule", cascade="all, delete-orphan")
    alerts = relationship("Alert", backref="rule")

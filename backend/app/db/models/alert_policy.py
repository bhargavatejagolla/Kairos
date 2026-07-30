from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import AuditMixin, TimestampMixin, UUIDPrimaryKeyMixin


class AlertPolicy(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "alert_policies"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    escalation_policy_id = Column(ForeignKey("escalation_policies.id", ondelete="SET NULL"), nullable=True)
    
    name = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    auto_create_incident = Column(Boolean, default=False, nullable=False)
    auto_resolve = Column(Boolean, default=True, nullable=False)
    deduplicate = Column(Boolean, default=True, nullable=False)
    
    correlation_window_seconds = Column(Integer, default=900, nullable=False) # 15 minutes
    
    organization = relationship("Organization")
    project = relationship("Project")
    escalation_policy = relationship("EscalationPolicy")

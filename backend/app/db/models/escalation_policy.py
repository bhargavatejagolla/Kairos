from sqlalchemy import Column, String, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin
from app.db.models.enums import EscalationStrategy

class EscalationPolicy(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "escalation_policies"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    strategy = Column(Enum(EscalationStrategy), nullable=False, default=EscalationStrategy.LINEAR)
    
    delay_minutes = Column(Integer, nullable=False, default=5)
    repeat_every = Column(Integer, nullable=True)
    max_escalations = Column(Integer, nullable=False, default=3)
    
    organization = relationship("Organization")

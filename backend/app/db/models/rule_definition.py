from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class RuleDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "rule_definitions"

    rule_id = Column(ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)
    
    # Store the full condition tree and aggregations as JSON for historical accuracy
    conditions_payload = Column(JSON, nullable=False)
    
    conditions = relationship("AlertCondition", backref="definition", cascade="all, delete-orphan")

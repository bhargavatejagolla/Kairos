from sqlalchemy import Column, String, ForeignKey, Enum, Float, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin
from app.db.models.enums import SignalType, AlertOperator, AggregationType

class AlertCondition(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "alert_conditions"

    definition_id = Column(ForeignKey("rule_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    signal_type = Column(Enum(SignalType), nullable=False)
    metric_name = Column(String(255), nullable=True) # E.g., cpu_usage, memory_bytes
    
    operator = Column(Enum(AlertOperator), nullable=False)
    threshold = Column(Float, nullable=False)
    
    aggregation = Column(Enum(AggregationType), nullable=True)
    duration_seconds = Column(Integer, nullable=False, default=300)

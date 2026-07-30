from sqlalchemy import JSON, Column, DateTime, Enum, Float, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.enums import AlertSource, SignalType
from app.db.models.mixins import UUIDPrimaryKeyMixin


class Signal(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "signals"

    service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    
    signal_type = Column(Enum(SignalType), nullable=False, index=True)
    source = Column(Enum(AlertSource), nullable=False)
    
    value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    
    received_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    __table_args__ = (
        Index("ix_signals_service_type_time", "service_id", "signal_type", "received_at"),
    )
    
    service = relationship("Service", backref="signals")

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AlertCorrelation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "alert_correlations"

    alert_id = Column(ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False, index=True)
    group_id = Column(ForeignKey("alert_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    
    reason = Column(String)
    score = Column(Float, nullable=False, default=1.0)
    
    alert = relationship("Alert")

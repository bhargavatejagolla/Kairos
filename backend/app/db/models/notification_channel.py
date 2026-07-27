from sqlalchemy import Column, String, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin
from app.db.models.enums import NotificationChannelType

class NotificationChannel(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "notification_channels"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    channel_type = Column(Enum(NotificationChannelType), nullable=False)
    
    configuration = Column(JSON, nullable=False) # e.g. webhook URL, slack token
    enabled = Column(Boolean, default=True, nullable=False)
    
    organization = relationship("Organization")

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.models.base import Base
from app.audit.enums.resource_type import ResourceType

class AuditTarget(Base):
    """
    Represents the resources affected by an audit action.
    A single action might affect multiple targets.
    """
    __tablename__ = "audit_targets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_log_id = Column(UUID(as_uuid=True), ForeignKey("audit_logs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    resource_type = Column(SQLEnum(ResourceType), nullable=False, index=True)
    resource_id = Column(String, nullable=True, index=True) # UUID string
    resource_name = Column(String, nullable=True)
    
    audit_log = relationship("AuditLog", back_populates="targets")

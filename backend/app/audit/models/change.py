import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AuditChange(Base):
    """
    Captures before and after states for fine-grained diffing.
    """
    __tablename__ = "audit_changes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_log_id = Column(UUID(as_uuid=True), ForeignKey("audit_logs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    field_name = Column(String, nullable=False)
    old_value = Column(JSONB, nullable=True)
    new_value = Column(JSONB, nullable=True)
    
    audit_log = relationship("AuditLog", back_populates="changes")

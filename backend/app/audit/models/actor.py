import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AuditActor(Base):
    __tablename__ = "audit_actors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_log_id = Column(UUID(as_uuid=True), ForeignKey("audit_logs.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    
    actor_type = Column(String, nullable=False) # e.g. "USER", "SYSTEM", "API_KEY"
    actor_id = Column(String, nullable=True, index=True) # UUID string or "system"
    actor_name = Column(String, nullable=True)
    actor_email = Column(String, nullable=True)
    
    audit_log = relationship("AuditLog", back_populates="actor")

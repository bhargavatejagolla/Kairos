from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.db.models.base import Base

class AuditMetadata(Base):
    """
    Stores flexible contextual payload for the event (e.g. queue name, AI model, exact payload).
    """
    __tablename__ = "audit_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_log_id = Column(UUID(as_uuid=True), ForeignKey("audit_logs.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    
    metadata_json = Column(JSONB, nullable=False, server_default='{}')
    
    audit_log = relationship("AuditLog", back_populates="metadata_info")

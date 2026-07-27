from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, UTC

from app.db.models.base import Base

class AuditExport(Base):
    """
    Tracks bulk exports of audit logs.
    """
    __tablename__ = "audit_exports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    requested_by_id = Column(UUID(as_uuid=True), nullable=False)
    
    status = Column(String, nullable=False, default="PENDING") # PENDING, PROCESSING, COMPLETED, FAILED
    format = Column(String, nullable=False) # CSV, PDF, JSON
    
    file_path = Column(String, nullable=True) # Populated when completed
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

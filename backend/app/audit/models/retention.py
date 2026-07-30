import uuid

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db.models.base import Base


class AuditRetentionPolicy(Base):
    """
    Organization-specific retention settings.
    """
    __tablename__ = "audit_retention_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), unique=True, index=True, nullable=False)
    
    retention_days = Column(Integer, nullable=False, default=90)
    archive_enabled = Column(Boolean, nullable=False, default=False)
    compression_enabled = Column(Boolean, nullable=False, default=True)
    delete_after_archive = Column(Boolean, nullable=False, default=True)

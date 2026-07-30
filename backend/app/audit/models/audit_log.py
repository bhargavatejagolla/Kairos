import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Index, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.audit.enums.action import AuditAction
from app.audit.enums.severity import AuditSeverity
from app.audit.enums.source import AuditSource
from app.audit.enums.status import AuditStatus
from app.db.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), index=True, nullable=True)
    project_id = Column(UUID(as_uuid=True), index=True, nullable=True)
    environment_id = Column(UUID(as_uuid=True), index=True, nullable=True)
    service_id = Column(UUID(as_uuid=True), index=True, nullable=True)
    
    correlation_id = Column(String, index=True, nullable=True)
    request_id = Column(String, index=True, nullable=True)
    
    event_type = Column(String, nullable=False, index=True) # e.g. "IncidentCreated"
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    
    status = Column(SQLEnum(AuditStatus), nullable=False)
    severity = Column(SQLEnum(AuditSeverity), nullable=False)
    source = Column(SQLEnum(AuditSource), nullable=False)
    
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Hash chaining for tamper detection
    previous_hash = Column(String, nullable=True)
    record_hash = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False, index=True)

    # Relationships
    actor = relationship("AuditActor", back_populates="audit_log", uselist=False, cascade="all, delete-orphan")
    targets = relationship("AuditTarget", back_populates="audit_log", cascade="all, delete-orphan")
    changes = relationship("AuditChange", back_populates="audit_log", cascade="all, delete-orphan")
    metadata_info = relationship("AuditMetadata", back_populates="audit_log", uselist=False, cascade="all, delete-orphan")
    attachments = relationship("AuditAttachment", back_populates="audit_log", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_audit_logs_org_created", "organization_id", "created_at"),
        Index("ix_audit_logs_correlation", "correlation_id"),
    )

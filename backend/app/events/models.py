import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.models.base import Base


class EventOutbox(Base):
    """
    Transactional outbox for reliable domain event publishing.
    Events are committed in the same database transaction as business logic.
    A background worker will pick these up and publish them to the EventBus.
    """
    __tablename__ = "event_outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSON, nullable=False)
    
    published = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    correlation_id = Column(String, nullable=True, index=True)

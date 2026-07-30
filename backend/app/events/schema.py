import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """
    Standardized Domain Event Contract.
    Every event across KAIROS uses this payload structure.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    organization_id: str | None = None
    project_id: str | None = None
    
    resource_type: str
    resource_id: str
    
    actor_id: str | None = None
    correlation_id: str | None = None
    request_id: str | None = None
    
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

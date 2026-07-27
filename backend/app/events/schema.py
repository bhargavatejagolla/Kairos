from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime, UTC
import uuid

class DomainEvent(BaseModel):
    """
    Standardized Domain Event Contract.
    Every event across KAIROS uses this payload structure.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    
    resource_type: str
    resource_id: str
    
    actor_id: Optional[str] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

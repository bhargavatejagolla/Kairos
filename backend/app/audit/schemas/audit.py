from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from app.audit.enums.action import AuditAction
from app.audit.enums.severity import AuditSeverity
from app.audit.enums.source import AuditSource
from app.audit.enums.status import AuditStatus
from app.audit.enums.resource_type import ResourceType

class AuditActorSchema(BaseModel):
    actor_type: str
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None
    actor_email: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditTargetSchema(BaseModel):
    resource_type: ResourceType
    resource_id: Optional[str] = None
    resource_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditChangeSchema(BaseModel):
    field_name: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditLogResponse(BaseModel):
    id: UUID
    organization_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    environment_id: Optional[UUID] = None
    service_id: Optional[UUID] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    
    event_type: str
    action: AuditAction
    status: AuditStatus
    severity: AuditSeverity
    source: AuditSource
    
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    created_at: datetime
    
    actor: Optional[AuditActorSchema] = None
    targets: List[AuditTargetSchema] = []
    changes: List[AuditChangeSchema] = []
    
    model_config = ConfigDict(from_attributes=True)

class AuditEventCreate(BaseModel):
    """
    Standardized Domain Event payload that modules emit.
    """
    organization_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    environment_id: Optional[UUID] = None
    service_id: Optional[UUID] = None
    
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    
    event_type: str
    action: AuditAction
    status: AuditStatus = AuditStatus.SUCCESS
    severity: AuditSeverity = AuditSeverity.INFO
    source: AuditSource = AuditSource.SYSTEM
    
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    actor_type: str = "SYSTEM"
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None
    actor_email: Optional[str] = None
    
    targets: List[AuditTargetSchema] = Field(default_factory=list)
    changes: List[AuditChangeSchema] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

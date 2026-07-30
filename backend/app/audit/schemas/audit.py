from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.audit.enums.action import AuditAction
from app.audit.enums.resource_type import ResourceType
from app.audit.enums.severity import AuditSeverity
from app.audit.enums.source import AuditSource
from app.audit.enums.status import AuditStatus


class AuditActorSchema(BaseModel):
    actor_type: str
    actor_id: str | None = None
    actor_name: str | None = None
    actor_email: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditTargetSchema(BaseModel):
    resource_type: ResourceType
    resource_id: str | None = None
    resource_name: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditChangeSchema(BaseModel):
    field_name: str
    old_value: Any | None = None
    new_value: Any | None = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditLogResponse(BaseModel):
    id: UUID
    organization_id: UUID | None = None
    project_id: UUID | None = None
    environment_id: UUID | None = None
    service_id: UUID | None = None
    correlation_id: str | None = None
    request_id: str | None = None
    
    event_type: str
    action: AuditAction
    status: AuditStatus
    severity: AuditSeverity
    source: AuditSource
    
    ip_address: str | None = None
    user_agent: str | None = None
    
    created_at: datetime
    
    actor: AuditActorSchema | None = None
    targets: list[AuditTargetSchema] = []
    changes: list[AuditChangeSchema] = []
    
    model_config = ConfigDict(from_attributes=True)

class AuditEventCreate(BaseModel):
    """
    Standardized Domain Event payload that modules emit.
    """
    organization_id: UUID | None = None
    project_id: UUID | None = None
    environment_id: UUID | None = None
    service_id: UUID | None = None
    
    correlation_id: str | None = None
    request_id: str | None = None
    
    event_type: str
    action: AuditAction
    status: AuditStatus = AuditStatus.SUCCESS
    severity: AuditSeverity = AuditSeverity.INFO
    source: AuditSource = AuditSource.SYSTEM
    
    ip_address: str | None = None
    user_agent: str | None = None
    
    actor_type: str = "SYSTEM"
    actor_id: str | None = None
    actor_name: str | None = None
    actor_email: str | None = None
    
    targets: list[AuditTargetSchema] = Field(default_factory=list)
    changes: list[AuditChangeSchema] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

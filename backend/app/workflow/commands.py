from uuid import UUID
from typing import Optional, Dict, Any
from app.core.command_bus import Command
from app.db.models.enums import IncidentStatus, IncidentSeverity, IncidentPriority, IncidentSource
from app.schemas.incident import IncidentCreate

class CreateIncidentCommand(Command):
    service_id: UUID
    organization_id: UUID
    project_id: UUID
    title: str
    description: str
    severity: IncidentSeverity = IncidentSeverity.SEV_3
    priority: IncidentPriority = IncidentPriority.P3
    source: IncidentSource = IncidentSource.MANUAL
    actor_id: Optional[UUID] = None
    
    @property
    def create_schema(self) -> IncidentCreate:
        return IncidentCreate(
            title=self.title,
            description=self.description,
            service_id=self.service_id,
            severity=self.severity,
            priority=self.priority,
            source=self.source
        )

class UpdateIncidentStatusCommand(Command):
    incident_id: UUID
    target_status: IncidentStatus
    actor_id: UUID
    message: Optional[str] = None
    metadata: Dict[str, Any] = {}

class AcknowledgeIncidentCommand(UpdateIncidentStatusCommand):
    target_status: IncidentStatus = IncidentStatus.ACKNOWLEDGED

class ResolveIncidentCommand(UpdateIncidentStatusCommand):
    target_status: IncidentStatus = IncidentStatus.RESOLVED

class MitigateIncidentCommand(UpdateIncidentStatusCommand):
    target_status: IncidentStatus = IncidentStatus.MITIGATED

class CloseIncidentCommand(UpdateIncidentStatusCommand):
    target_status: IncidentStatus = IncidentStatus.CLOSED

class AssignIncidentCommand(Command):
    incident_id: UUID
    assignee_id: UUID
    actor_id: UUID

from typing import Dict, Any
from uuid import UUID

from app.core.command_bus import CommandHandler, command_bus
from app.workflow.commands import (
    CreateIncidentCommand, 
    UpdateIncidentStatusCommand,
    AssignIncidentCommand
)
from app.services.incident_service import IncidentService
from app.services.assignment_service import AssignmentService
from app.db.models.incident import Incident
from app.core.project_context import ProjectContext
from app.db.models.organization import Organization
from app.db.models.project import Project

class CreateIncidentHandler(CommandHandler[CreateIncidentCommand, Incident]):
    def __init__(self, incident_service: IncidentService):
        self.incident_service = incident_service

    async def handle(self, command: CreateIncidentCommand) -> Incident:
        # Reconstruct a basic context for the service (in a real app, you might pass it directly or load it)
        # For simplicity, IncidentService.create expects a ProjectContext-like object with org_id and project_id.
        class _MockContext:
            organization_id = command.organization_id
            project_id = command.project_id
            
        return await self.incident_service.create(
            context=_MockContext(), 
            data=command.create_schema, 
            created_by=command.actor_id
        )

class UpdateIncidentStatusHandler(CommandHandler[UpdateIncidentStatusCommand, Incident]):
    def __init__(self, incident_service: IncidentService):
        self.incident_service = incident_service

    async def handle(self, command: UpdateIncidentStatusCommand) -> Incident:
        incident = await self.incident_service.get_by_id(command.incident_id)
        # Note: the timeline message and metadata should ideally be passed down.
        # But for now, update_status will trigger the state machine which adds a timeline entry.
        return await self.incident_service.update_status(
            incident=incident, 
            target_status=command.target_status, 
            updated_by=command.actor_id
        )

class AssignIncidentHandler(CommandHandler[AssignIncidentCommand, Incident]):
    def __init__(self, incident_service: IncidentService, assignment_service: AssignmentService):
        self.incident_service = incident_service
        self.assignment_service = assignment_service
        
    async def handle(self, command: AssignIncidentCommand) -> Incident:
        incident = await self.incident_service.get_by_id(command.incident_id)
        return await self.assignment_service.assign_incident(incident, command.assignee_id)

# Helper to register all handlers manually or via a DI container.
def register_incident_handlers(incident_service: IncidentService, assignment_service: AssignmentService):
    command_bus.register(CreateIncidentCommand, CreateIncidentHandler(incident_service))
    # Register base status updates (they inherit so we must register subclasses if they are used as types, 
    # but since the API will dispatch the specific subclass, we can register them specifically or 
    # make the endpoint instantiate the base class).
    status_handler = UpdateIncidentStatusHandler(incident_service)
    command_bus.register(UpdateIncidentStatusCommand, status_handler)
    from app.workflow.commands import (AcknowledgeIncidentCommand, ResolveIncidentCommand, 
                                     MitigateIncidentCommand, CloseIncidentCommand)
    command_bus.register(AcknowledgeIncidentCommand, status_handler)
    command_bus.register(ResolveIncidentCommand, status_handler)
    command_bus.register(MitigateIncidentCommand, status_handler)
    command_bus.register(CloseIncidentCommand, status_handler)
    
    command_bus.register(AssignIncidentCommand, AssignIncidentHandler(incident_service, assignment_service))

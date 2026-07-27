from uuid import UUID
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException as ResourceNotFoundError
from app.db.models.incident import Incident
from app.db.models.enums import IncidentStatus, TimelineEvent
from app.repositories.incident import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentUpdate
from app.core.organization_context import OrganizationContext
from app.core.project_context import ProjectContext
from app.core.state_machine import StateMachine, StateTransitionError
from app.core.workflow import WorkflowEngine
from app.services.timeline_service import TimelineService

class IncidentStateMachine(StateMachine[IncidentStatus, Incident]):
    def __init__(self, timeline_service: TimelineService):
        super().__init__({
            IncidentStatus.OPEN: [IncidentStatus.ACKNOWLEDGED, IncidentStatus.INVESTIGATING, IncidentStatus.MITIGATED, IncidentStatus.RESOLVED, IncidentStatus.CLOSED],
            IncidentStatus.ACKNOWLEDGED: [IncidentStatus.INVESTIGATING, IncidentStatus.MITIGATED, IncidentStatus.RESOLVED, IncidentStatus.CLOSED],
            IncidentStatus.INVESTIGATING: [IncidentStatus.MITIGATED, IncidentStatus.RESOLVED, IncidentStatus.CLOSED],
            IncidentStatus.MITIGATED: [IncidentStatus.RESOLVED, IncidentStatus.INVESTIGATING, IncidentStatus.CLOSED],
            IncidentStatus.RESOLVED: [IncidentStatus.CLOSED, IncidentStatus.INVESTIGATING],
            IncidentStatus.CLOSED: [IncidentStatus.INVESTIGATING] # can reopen
        })
        self.timeline = timeline_service
        self._setup_hooks()
        
    def _setup_hooks(self):
        async def record_acknowledged(incident: Incident, session: AsyncSession):
            incident.acknowledged_at = datetime.now(UTC)
            await self.timeline.add_entry(incident.id, TimelineEvent.ACKNOWLEDGED, incident.updated_by_id)

        async def record_mitigated(incident: Incident, session: AsyncSession):
            incident.mitigated_at = datetime.now(UTC)
            await self.timeline.add_entry(incident.id, TimelineEvent.MITIGATED, incident.updated_by_id)

        async def record_resolved(incident: Incident, session: AsyncSession):
            incident.resolved_at = datetime.now(UTC)
            await self.timeline.add_entry(incident.id, TimelineEvent.RESOLVED, incident.updated_by_id)

        async def record_closed(incident: Incident, session: AsyncSession):
            incident.closed_at = datetime.now(UTC)
            await self.timeline.add_entry(incident.id, TimelineEvent.CLOSED, incident.updated_by_id)

        # Before transitioning to ACKNOWLEDGED from anywhere
        for current_state in self.allowed_transitions:
            if IncidentStatus.ACKNOWLEDGED in self.allowed_transitions[current_state]:
                self.add_hook(current_state, IncidentStatus.ACKNOWLEDGED, record_acknowledged, "before")
            if IncidentStatus.MITIGATED in self.allowed_transitions[current_state]:
                self.add_hook(current_state, IncidentStatus.MITIGATED, record_mitigated, "before")
            if IncidentStatus.RESOLVED in self.allowed_transitions[current_state]:
                self.add_hook(current_state, IncidentStatus.RESOLVED, record_resolved, "before")
            if IncidentStatus.CLOSED in self.allowed_transitions[current_state]:
                self.add_hook(current_state, IncidentStatus.CLOSED, record_closed, "before")

class IncidentService:
    def __init__(
        self, 
        repository: IncidentRepository, 
        timeline_service: TimelineService, 
        workflow_engine: WorkflowEngine,
        session: AsyncSession
    ):
        self.repository = repository
        self.timeline = timeline_service
        self.workflow = workflow_engine
        self.state_machine = IncidentStateMachine(timeline_service)
        self.session = session

    async def get_by_id(self, incident_id: UUID) -> Incident:
        incident = await self.repository.get(incident_id)
        if not incident:
            raise ResourceNotFoundError(f"Incident {incident_id} not found")
        return incident

    async def create(self, context: ProjectContext, data: IncidentCreate, created_by: UUID | None = None) -> Incident:
        # Generate number - in reality this would use a sequence or better counter per org
        inc_count = await self.repository.count_by_service(data.service_id)
        number = f"INC-{context.organization_id.hex[:4].upper()}-{inc_count + 1}"
        
        incident = Incident(
            organization_id=context.organization_id,
            project_id=context.project_id,
            number=number,
            created_by_id=created_by,
            detected_at=datetime.now(UTC),
            **data.model_dump()
        )
        await self.repository.add(incident)
        
        await self.timeline.add_entry(
            incident.id, 
            TimelineEvent.CREATED, 
            actor_id=created_by, 
            message=f"Incident {number} created.",
            metadata={"source": data.source.value}
        )
        
        # Trigger workflow
        await self.workflow.process_transition(
            "Incident", 
            str(incident.id), 
            None, 
            IncidentStatus.OPEN, 
            self.session,
            {"title": data.title}
        )
        
        # Transactional Outbox for Domain Events
        from app.events.outbox_service import OutboxService
        from app.events.schema import DomainEvent
        from app.middleware.correlation import correlation_id_var
        
        outbox = OutboxService(self.session)
        event = DomainEvent(
            event_type="IncidentCreated",
            organization_id=str(context.organization_id),
            project_id=str(context.project_id),
            resource_type="INCIDENT",
            resource_id=str(incident.id),
            actor_id=str(created_by) if created_by else None,
            correlation_id=correlation_id_var.get(None),
            payload={
                "title": data.title,
                "priority": "P1",
                "assigned_to": str(incident.assigned_to) if hasattr(incident, "assigned_to") and incident.assigned_to else None
            }
        )
        await outbox.save_event(event)
        
        return incident

    async def update_status(self, incident: Incident, target_status: IncidentStatus, updated_by: UUID) -> Incident:
        if incident.status == target_status:
            return incident
            
        current_status = incident.status
        incident.updated_by_id = updated_by
        
        await self.state_machine.execute_transition(incident, current_status, target_status, self.session)
        incident.status = target_status
        await self.repository.update(incident)
        
        # In reality, status change timeline is added via state machine or here if it's general
        if target_status not in [IncidentStatus.ACKNOWLEDGED, IncidentStatus.MITIGATED, IncidentStatus.RESOLVED, IncidentStatus.CLOSED]:
             await self.timeline.add_entry(
                 incident.id, 
                 TimelineEvent.STATUS_CHANGED, 
                 actor_id=updated_by, 
                 metadata={"previous": current_status.value, "new": target_status.value}
             )
             
        await self.workflow.process_transition(
            "Incident",
            str(incident.id),
            current_status,
            target_status,
            self.session
        )
        
        return incident

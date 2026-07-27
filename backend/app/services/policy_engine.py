import logging
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.db.models.alert_group import AlertGroup
from app.repositories.alert_policy import AlertPolicyRepository
from app.services.escalation_engine import EscalationEngine

logger = logging.getLogger(__name__)

class PolicyEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.policy_repo = AlertPolicyRepository(session)
        self.escalation_engine = EscalationEngine(session)
        # Note: IncidentService would be injected here for auto-incident creation

    async def apply(self, organization_id: UUID, project_id: UUID, alert: Alert, group: AlertGroup) -> None:
        """
        Determines the routing behavior (Escalation / Incident Creation).
        """
        policies = await self.policy_repo.list_by_project(project_id)
        # In a real system, we'd match tags. For now, use the default policy.
        policy = next((p for p in policies if p.is_default), None)
        
        if not policy:
            return
            
        if policy.auto_create_incident and not group.incident_id:
            # Here we would call the Incident Workflow from Phase 9
            # incident = await self.incident_service.create(...)
            # alert.incident_id = incident.id
            pass
            
        if policy.escalation_policy_id:
            await self.escalation_engine.schedule(organization_id, policy.escalation_policy_id, alert)

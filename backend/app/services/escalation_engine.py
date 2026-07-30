import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.repositories.escalation_policy import EscalationPolicyRepository
from app.services.notification_router import NotificationRouter

logger = logging.getLogger(__name__)

class EscalationEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.escalation_repo = EscalationPolicyRepository(session)
        self.notification_router = NotificationRouter(session)

    async def schedule(self, organization_id: UUID, escalation_policy_id: UUID, alert: Alert) -> None:
        """
        Schedules the initial notification and sets up retry loops.
        """
        policy = await self.escalation_repo.get(escalation_policy_id)
        if not policy:
            return
            
        # For this stub, immediately route. In production this would push a job to Redis/Celery.
        await self.notification_router.route(organization_id, alert)
        
        # Future: Schedule next step in `policy.delay_minutes`

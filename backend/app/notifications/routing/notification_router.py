from uuid import UUID
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifications.routing.recipient_resolver import RecipientResolver
from app.notifications.routing.policy_engine import PolicyEngine
from app.notifications.schemas.notification import NotificationCreate
from app.notifications.workflows.notification_workflow import NotificationWorkflow
from app.notifications.enums.category import NotificationCategory
from app.notifications.enums.priority import NotificationPriority

logger = structlog.get_logger(__name__)

class NotificationRouter:
    """
    Central dispatcher. Listens to domain events and maps them to recipients and templates.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.resolver = RecipientResolver(session)
        self.policy_engine = PolicyEngine(session)
        self.workflow = NotificationWorkflow(session)

    async def dispatch_event(self, event_type: str, payload: dict):
        logger.info("routing_notification_event", event_type=event_type)
        
        organization_id = payload.get("organization_id")
        
        if event_type == "IncidentCreated":
            await self._handle_incident_created(organization_id, payload)
        elif event_type == "AlertTriggered":
            await self._handle_alert_triggered(organization_id, payload)
        elif event_type == "UserRegistered":
            await self._handle_user_registered(organization_id, payload)
        else:
            logger.debug("no_notification_route", event_type=event_type)

    async def _handle_incident_created(self, org_id: str, payload: dict):
        # In DomainEvent, incident_id is in resource_id, and specific details are in payload["payload"]
        incident_id_str = payload.get("resource_id") or payload.get("payload", {}).get("incident_id")
        incident_id = UUID(incident_id_str)
        recipients = await self.resolver.get_incident_recipients(incident_id)
        
        for user_id in recipients:
            if await self.policy_engine.evaluate(user_id, NotificationCategory.INCIDENT, deduplication_key=f"inc_{incident_id}"):
                notification_in = NotificationCreate(
                    organization_id=UUID(org_id),
                    recipient_user_id=user_id,
                    event_type="IncidentCreated",
                    category=NotificationCategory.INCIDENT,
                    priority=NotificationPriority.HIGH,
                    payload=payload.get("payload", payload)
                )
                await self.workflow.dispatch(notification_in, template_slug="incident-created")

    async def _handle_alert_triggered(self, org_id: str, payload: dict):
        alert_id_str = payload.get("resource_id") or payload.get("payload", {}).get("alert_id")
        alert_id = alert_id_str
        # Notify all admins for critical alerts
        recipients = await self.resolver.get_org_admins(UUID(org_id))
        
        for user_id in recipients:
            # Prevent spam if the same alert fires multiple times
            if await self.policy_engine.evaluate(user_id, NotificationCategory.ALERT, deduplication_key=f"alert_{alert_id}"):
                notification_in = NotificationCreate(
                    organization_id=UUID(org_id),
                    recipient_user_id=user_id,
                    event_type="AlertTriggered",
                    category=NotificationCategory.ALERT,
                    priority=NotificationPriority.CRITICAL,
                    payload=payload.get("payload", payload)
                )
                await self.workflow.dispatch(notification_in, template_slug="alert-triggered")

    async def _handle_user_registered(self, org_id: str | None, payload: dict):
        user_id_str = payload.get("resource_id") or payload.get("payload", {}).get("user_id")
        user_id = UUID(user_id_str)
        recipients = await self.resolver.get_user_by_id(user_id)
        
        for uid in recipients:
            if await self.policy_engine.evaluate(uid, NotificationCategory.USER):
                notification_in = NotificationCreate(
                    organization_id=UUID(org_id) if org_id else user_id, # Fallback to user_id as namespace if no org
                    recipient_user_id=uid,
                    event_type="UserRegistered",
                    category=NotificationCategory.USER,
                    priority=NotificationPriority.NORMAL,
                    payload=payload
                )
                await self.workflow.dispatch(notification_in, template_slug="welcome-email")

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.notifications.services.notification_service import NotificationService
from app.notifications.services.template_service import TemplateService
from app.notifications.services.preference_service import PreferenceService
from app.notifications.schemas.notification import NotificationCreate
from app.notifications.enums.status import NotificationStatus
from app.notifications.models.notification import Notification
# We import background tasks to enqueue the email job
from app.background.celery_app import celery_app

logger = structlog.get_logger(__name__)

class NotificationWorkflow:
    def __init__(self, session: AsyncSession):
        self.notification_service = NotificationService(session)
        self.template_service = TemplateService(session)
        self.preference_service = PreferenceService(session)

    async def dispatch(self, notification_in: NotificationCreate, template_slug: str) -> Notification | None:
        """
        Create -> Validate -> Template -> Queue
        """
        # 1. Validate Preferences
        if notification_in.recipient_user_id:
            is_enabled = await self.preference_service.is_enabled(
                notification_in.recipient_user_id, 
                notification_in.category.value
            )
            if not is_enabled:
                logger.info("notification_skipped_by_preference", user_id=str(notification_in.recipient_user_id))
                return None

        # 2. Assign Template
        template = await self.template_service.get_by_slug(template_slug, notification_in.organization_id)
        if template:
            notification_in.template_id = template.id
            if not notification_in.subject:
                # Can be rendered later, but save base for now
                notification_in.subject = template.subject_template
        else:
            logger.error("template_not_found", slug=template_slug)
            return None

        # 3. Create Notification
        notification = await self.notification_service.create(notification_in)

        # 4. Queue Background Job
        await self.queue(notification.id)
        
        return notification

    async def queue(self, notification_id: UUID):
        # Update status
        await self.notification_service.update_status(notification_id, NotificationStatus.QUEUED)
        
        # Dispatch to Celery (Phase 12 Background Processing)
        # We will create this job in app/notifications/jobs/send_email.py
        celery_app.send_task(
            "notifications.send_email",
            args=[str(notification_id)],
            queue="notifications"
        )

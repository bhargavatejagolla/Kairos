import time
from uuid import UUID

import structlog
from prometheus_client import Counter, Histogram

from app.background.jobs.base_job import BaseJob
from app.db.session import SessionLocal
from app.notifications.email.renderer import TemplateEngine
from app.notifications.enums.status import NotificationStatus
from app.notifications.providers.smtp_provider import SMTPProvider
from app.notifications.services.notification_service import NotificationService
from app.notifications.services.template_service import TemplateService
from app.repositories.user import UserRepository

EMAILS_SENT_TOTAL = Counter('emails_sent_total', 'Total emails successfully sent')
EMAILS_FAILED_TOTAL = Counter('emails_failed_total', 'Total emails failed to send')
TEMPLATE_RENDER_TIME = Histogram('template_render_time_seconds', 'Time taken to render templates')

logger = structlog.get_logger(__name__)

class SendEmailJob(BaseJob):
    name = "notifications.send_email"
    queue = "notifications"
    
    def __init__(self):
        super().__init__()
        self.provider = SMTPProvider()
        self.engine = TemplateEngine()

    async def run(self, notification_id: str, *args, **kwargs):
        nid = UUID(notification_id)
        
        async with SessionLocal() as session:
            notification_service = NotificationService(session)
            template_service = TemplateService(session)
            user_repo = UserRepository(session)
            
            # 1. Fetch Notification
            notification = await notification_service.get(nid)
            if not notification or notification.status == NotificationStatus.SENT:
                return {"status": "skipped", "reason": "Not found or already sent"}
                
            await notification_service.update_status(nid, NotificationStatus.RENDERING)
            
            try:
                # 2. Render Template
                template = await template_service.repository.get_by_id(notification.template_id)
                recipient = await user_repo.get_by_id(notification.recipient_user_id)
                
                if not recipient or not recipient.email:
                    await notification_service.update_status(nid, NotificationStatus.FAILED)
                    await notification_service.audit(nid, "Recipient missing email", "system")
                    return {"status": "failed", "reason": "No recipient email"}
                
                context = notification.payload or {}
                context["user_name"] = recipient.full_name or recipient.email
                
                # Render HTML and Subject
                render_start = time.time()
                html_content = self.engine.render(template.html_template, context)
                subject = self.engine.render(template.subject_template, context)
                text_content = self.engine.render(template.text_template, context) if template.text_template else None
                TEMPLATE_RENDER_TIME.observe(time.time() - render_start)
                
                await notification_service.update_status(nid, NotificationStatus.SENDING)
                
                # 3. Dispatch via SMTP
                start_time = time.time()
                success = await self.provider.send_email(
                    to_email=recipient.email,
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content
                )
                duration_ms = int((time.time() - start_time) * 1000)
                
                if success:
                    await notification_service.update_status(nid, NotificationStatus.SENT)
                    await notification_service.record_delivery_attempt(nid, "SMTP", "SUCCESS", duration_ms)
                    EMAILS_SENT_TOTAL.inc()
                    return {"status": "success"}
                    
            except Exception as e:
                logger.error("email_send_failed", notification_id=notification_id, error=str(e))
                await notification_service.update_status(nid, NotificationStatus.FAILED)
                await notification_service.record_delivery_attempt(nid, "SMTP", "FAILED", 0, error_message=str(e))
                EMAILS_FAILED_TOTAL.inc()
                raise # Raise to trigger Celery Retry / DLQ mechanisms

# Celery task registration
send_email_task = SendEmailJob()

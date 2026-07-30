from email.message import EmailMessage

import aiosmtplib
import structlog

from app.notifications.config.smtp import smtp_config
from app.notifications.providers.base_provider import EmailProvider

logger = structlog.get_logger(__name__)

class SMTPProvider(EmailProvider):
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str | None = None
    ) -> bool:
        message = EmailMessage()
        message["From"] = f"{smtp_config.from_name} <{smtp_config.from_email}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        if text_content:
            message.set_content(text_content)
            message.add_alternative(html_content, subtype="html")
        else:
            message.set_content(html_content, subtype="html")
            
        try:
            await aiosmtplib.send(
                message,
                hostname=smtp_config.host,
                port=smtp_config.port,
                username=smtp_config.user,
                password=smtp_config.password,
                start_tls=smtp_config.use_tls
            )
            logger.info("email_sent", to=to_email, subject=subject)
            return True
        except Exception as e:
            logger.error("email_send_failed", error=str(e), to=to_email)
            raise

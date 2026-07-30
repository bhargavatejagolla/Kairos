import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.db.models.enums import NotificationChannelType
from app.repositories.notification_channel import NotificationChannelRepository

logger = logging.getLogger(__name__)

class NotificationRouter:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.channel_repo = NotificationChannelRepository(session)

    async def route(self, organization_id: UUID, alert: Alert) -> None:
        """
        Routes the alert to all configured notification channels for the organization.
        """
        channels = await self.channel_repo.list_by_organization(organization_id)
        
        for channel in channels:
            if channel.channel_type == NotificationChannelType.EMAIL:
                await self._email(channel, alert)
            elif channel.channel_type == NotificationChannelType.SLACK:
                await self._slack(channel, alert)
            elif channel.channel_type == NotificationChannelType.WEBHOOK:
                await self._webhook(channel, alert)
                
    async def _email(self, channel, alert: Alert) -> None:
        logger.info(f"Sending EMAIL to {channel.name} for alert {alert.id}")
        
    async def _slack(self, channel, alert: Alert) -> None:
        logger.info(f"Sending SLACK to {channel.name} for alert {alert.id}")
        
    async def _webhook(self, channel, alert: Alert) -> None:
        logger.info(f"Sending WEBHOOK to {channel.name} for alert {alert.id}")

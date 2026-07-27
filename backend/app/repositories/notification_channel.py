from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification_channel import NotificationChannel
from app.repositories.base import BaseRepository

class NotificationChannelRepository(BaseRepository[NotificationChannel]):
    def __init__(self, session: AsyncSession):
        super().__init__(NotificationChannel, session)

    async def list_by_organization(self, organization_id: UUID) -> Sequence[NotificationChannel]:
        stmt = select(NotificationChannel).where(
            NotificationChannel.organization_id == organization_id,
            NotificationChannel.enabled == True
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

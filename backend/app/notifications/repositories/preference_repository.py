from typing import Optional
from uuid import UUID
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.notifications.models.preference import NotificationPreference

class PreferenceRepository(BaseRepository[NotificationPreference]):
    def __init__(self, session):
        super().__init__(NotificationPreference, session)

    async def get_by_user_id(self, user_id: UUID) -> Optional[NotificationPreference]:
        stmt = select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

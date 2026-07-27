from uuid import UUID
from app.notifications.repositories.preference_repository import PreferenceRepository
from app.notifications.models.preference import NotificationPreference
from app.notifications.schemas.preference import NotificationPreferenceUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class PreferenceService:
    def __init__(self, session: AsyncSession):
        self.repository = PreferenceRepository(session)

    async def get_or_create(self, user_id: UUID) -> NotificationPreference:
        pref = await self.repository.get_by_user_id(user_id)
        if not pref:
            pref = await self.repository.create({"user_id": user_id})
        return pref

    async def update(self, user_id: UUID, preference_in: NotificationPreferenceUpdate) -> NotificationPreference:
        pref = await self.get_or_create(user_id)
        return await self.repository.update(pref.id, preference_in.model_dump(exclude_unset=True))

    async def is_enabled(self, user_id: UUID, category: str) -> bool:
        pref = await self.get_or_create(user_id)
        if category == "INCIDENT": return pref.incident_enabled
        if category == "ALERT": return pref.alert_enabled
        if category == "SECURITY": return pref.security_enabled
        if category == "SYSTEM": return pref.system_enabled
        if category == "REPORT": return pref.weekly_reports
        return True # Default to true for others

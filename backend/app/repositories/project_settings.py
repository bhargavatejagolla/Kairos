from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project_settings import ProjectSettings
from app.repositories.base import BaseRepository
from app.schemas.project_settings import ProjectSettingsUpdate


class ProjectSettingsRepository(BaseRepository[ProjectSettings]):
    def __init__(self, session: AsyncSession):
        super().__init__(ProjectSettings, session)

    async def get_by_project_id(self, project_id: UUID) -> ProjectSettings | None:
        statement = select(ProjectSettings).where(ProjectSettings.project_id == project_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def reset_defaults(self, project_id: UUID) -> ProjectSettings | None:
        settings = await self.get_by_project_id(project_id)
        if not settings:
            return None
            
        settings.timezone = "UTC"
        settings.retention_days = 30
        settings.ai_enabled = True
        settings.notifications_enabled = True
        settings.incident_auto_creation = False
        settings.default_severity = "SEV-3"
        settings.alert_grouping = "time_based"
        settings.tags = None
        
        self.session.add(settings)
        await self.session.flush()
        await self.session.refresh(settings)
        return settings

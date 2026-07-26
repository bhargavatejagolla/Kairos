from uuid import UUID

from app.core.exceptions import ProjectNotFoundError
from app.repositories.project_settings import ProjectSettingsRepository
from app.schemas.project_settings import ProjectSettingsUpdate

class ProjectSettingsService:
    def __init__(self, settings_repo: ProjectSettingsRepository):
        self.settings_repo = settings_repo

    async def get_settings(self, project_id: UUID):
        settings = await self.settings_repo.get_by_project_id(project_id)
        if not settings:
            raise ProjectNotFoundError("Project settings not found")
        return settings

    async def update_settings(self, project_id: UUID, data: ProjectSettingsUpdate):
        settings = await self.get_settings(project_id)
        return await self.settings_repo.update(settings, data)

    async def reset_defaults(self, project_id: UUID):
        return await self.settings_repo.reset_defaults(project_id)

    async def enable_ai(self, project_id: UUID):
        settings = await self.get_settings(project_id)
        return await self.settings_repo.update(settings, ProjectSettingsUpdate(ai_enabled=True))

    async def disable_ai(self, project_id: UUID):
        settings = await self.get_settings(project_id)
        return await self.settings_repo.update(settings, ProjectSettingsUpdate(ai_enabled=False))

    async def enable_notifications(self, project_id: UUID):
        settings = await self.get_settings(project_id)
        return await self.settings_repo.update(settings, ProjectSettingsUpdate(notifications_enabled=True))

    async def disable_notifications(self, project_id: UUID):
        settings = await self.get_settings(project_id)
        return await self.settings_repo.update(settings, ProjectSettingsUpdate(notifications_enabled=False))

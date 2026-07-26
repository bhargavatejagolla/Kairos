from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import event_bus
from app.core.exceptions import EnvironmentNotFoundError, InvalidProjectStateError, ProjectAlreadyExistsError, ProjectArchivedError, ProjectNotFoundError
from app.core.project import ProjectStatus
from app.db.models.project_settings import ProjectSettings
from app.repositories.environment import EnvironmentRepository
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        environment_repo: EnvironmentRepository,
        session: AsyncSession
    ):
        self.project_repo = project_repo
        self.environment_repo = environment_repo
        self.session = session

    async def create_project(self, organization_id: UUID, user_id: UUID, data: ProjectCreate):
        if await self.project_repo.exists(organization_id, data.slug):
            raise ProjectAlreadyExistsError()
            
        environment = await self.environment_repo.get_by_id(data.environment_id)
        if not environment or environment.organization_id != organization_id:
            raise EnvironmentNotFoundError()

        async with self.session.begin_nested():
            from app.db.models.project import Project
            from app.db.models.project_settings import ProjectSettings
            
            project = Project(
                organization_id=organization_id,
                created_by_id=user_id,
                updated_by_id=user_id,
                **data.model_dump()
            )
            self.session.add(project)
            await self.session.flush()
            
            # Create default settings
            settings = ProjectSettings(project_id=project.id)
            self.session.add(settings)
            
        # Emit Domain Event
        await event_bus.publish("ProjectCreated", {"project_id": str(project.id), "organization_id": str(organization_id)})
        
        # Reload with details (environment and settings)
        return await self.project_repo.get_with_details(project.id)

    async def get_project(self, organization_id: UUID, slug: str):
        project = await self.project_repo.get_by_slug(organization_id, slug)
        if not project:
            raise ProjectNotFoundError()
        return await self.project_repo.get_with_details(project.id)

    async def list_projects(
        self,
        organization_id: UUID,
        query: str | None = None,
        status: ProjectStatus | None = None,
        environment_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        return await self.project_repo.search(
            organization_id, 
            query=query, 
            status=status, 
            environment_id=environment_id, 
            skip=skip, 
            limit=limit
        )

    async def update_project(self, organization_id: UUID, slug: str, user_id: UUID, data: ProjectUpdate):
        project = await self.project_repo.get_by_slug(organization_id, slug)
        if not project:
            raise ProjectNotFoundError()

        if project.status == ProjectStatus.ARCHIVED and data.status != ProjectStatus.ACTIVE:
            raise ProjectArchivedError()

        if data.environment_id:
            env = await self.environment_repo.get_by_id(data.environment_id)
            if not env or env.organization_id != organization_id:
                raise EnvironmentNotFoundError()

        project.updated_by_id = user_id
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(project, key, value)
            
        await self.project_repo.update(project)
        return await self.project_repo.get_with_details(project.id)

    async def archive_project(self, organization_id: UUID, slug: str, user_id: UUID):
        project = await self.project_repo.get_by_slug(organization_id, slug)
        if not project:
            raise ProjectNotFoundError()
            
        if project.status == ProjectStatus.ARCHIVED:
            raise InvalidProjectStateError("Project is already archived")

        project.status = ProjectStatus.ARCHIVED
        project.updated_by_id = user_id
        await self.project_repo.update(project)
        
        await event_bus.publish("ProjectArchived", {"project_id": str(project.id)})
        return await self.project_repo.get_with_details(project.id)

    async def restore_project(self, organization_id: UUID, slug: str, user_id: UUID):
        project = await self.project_repo.get_by_slug(organization_id, slug)
        if not project:
            raise ProjectNotFoundError()
            
        if project.status != ProjectStatus.ARCHIVED:
            raise InvalidProjectStateError("Project is not archived")

        project.status = ProjectStatus.ACTIVE
        project.updated_by_id = user_id
        await self.project_repo.update(project)
        
        await event_bus.publish("ProjectRestored", {"project_id": str(project.id)})
        return await self.project_repo.get_with_details(project.id)

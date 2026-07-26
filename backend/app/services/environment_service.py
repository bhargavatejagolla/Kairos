from uuid import UUID

from app.core.exceptions import EnvironmentInUseError, EnvironmentNotFoundError
from app.repositories.environment import EnvironmentRepository
from app.repositories.project import ProjectRepository
from app.schemas.environment import EnvironmentCreate, EnvironmentUpdate
class EnvironmentService:
    def __init__(
        self, 
        environment_repo: EnvironmentRepository,
        project_repo: ProjectRepository
    ):
        self.environment_repo = environment_repo
        self.project_repo = project_repo

    async def create_environment(self, organization_id: UUID, data: EnvironmentCreate):
        if await self.environment_repo.exists(organization_id, data.slug):
            raise ValueError(f"Environment with slug '{data.slug}' already exists in this organization")
            
        from app.db.models.environment import Environment
        environment = Environment(
            organization_id=organization_id,
            **data.model_dump()
        )
        environment = await self.environment_repo.create(environment)
        return environment

    async def get_environment(self, organization_id: UUID, slug: str):
        environment = await self.environment_repo.get_by_slug(organization_id, slug)
        if not environment:
            raise EnvironmentNotFoundError()
        return environment

    async def update_environment(self, organization_id: UUID, slug: str, data: EnvironmentUpdate):
        environment = await self.get_environment(organization_id, slug)
        return await self.environment_repo.update(environment, data)

    async def delete_environment(self, organization_id: UUID, slug: str):
        if slug == "production":
            raise ValueError("Default environment 'production' cannot be deleted")

        environment = await self.get_environment(organization_id, slug)
        
        # Check if used by any projects
        # We can search by environment_id
        projects = await self.project_repo.search(
            organization_id=organization_id, 
            environment_id=environment.id,
            limit=1
        )
        if projects:
            raise EnvironmentInUseError()
            
        await self.environment_repo.delete(environment)

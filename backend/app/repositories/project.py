from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.project import ProjectStatus
from app.db.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)

    async def get_by_slug(self, organization_id: UUID, slug: str) -> Project | None:
        statement = select(Project).where(
            Project.organization_id == organization_id,
            Project.slug == slug
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def exists(self, organization_id: UUID, slug: str) -> bool:
        project = await self.get_by_slug(organization_id, slug)
        return project is not None
        
    async def get_with_details(self, project_id: UUID) -> Project | None:
        statement = (
            select(Project)
            .options(
                selectinload(Project.environment),
                selectinload(Project.settings),
            )
            .where(Project.id == project_id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_by_organization(
        self, 
        organization_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> Sequence[Project]:
        statement = (
            select(Project)
            .options(selectinload(Project.environment))
            .where(Project.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def search(
        self,
        organization_id: UUID,
        query: str | None = None,
        status: ProjectStatus | None = None,
        environment_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[Project]:
        statement = select(Project).options(selectinload(Project.environment)).where(Project.organization_id == organization_id)
        
        if query:
            statement = statement.where(
                (Project.name.ilike(f"%{query}%")) | (Project.slug.ilike(f"%{query}%"))
            )
        if status:
            statement = statement.where(Project.status == status)
        if environment_id:
            statement = statement.where(Project.environment_id == environment_id)
            
        statement = statement.offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def count_by_organization(self, organization_id: UUID) -> int:
        statement = select(func.count()).where(Project.organization_id == organization_id)
        result = await self.session.execute(statement)
        return result.scalar_one() or 0

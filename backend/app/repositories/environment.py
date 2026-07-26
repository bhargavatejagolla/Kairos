from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.environment import Environment
from app.repositories.base import BaseRepository
from app.schemas.environment import EnvironmentCreate, EnvironmentUpdate


class EnvironmentRepository(BaseRepository[Environment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Environment, session)

    async def get_by_slug(self, organization_id: UUID, slug: str) -> Environment | None:
        statement = select(Environment).where(
            Environment.organization_id == organization_id,
            Environment.slug == slug
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_default_environment(self, organization_id: UUID) -> Environment | None:
        # Assuming "production" is the default slug
        return await self.get_by_slug(organization_id, "production")

    async def exists(self, organization_id: UUID, slug: str) -> bool:
        env = await self.get_by_slug(organization_id, slug)
        return env is not None

from uuid import UUID
from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.db.models.service import Service

class ServiceRepository(BaseRepository[Service]):
    def __init__(self, session):
        super().__init__(Service, session)

    async def get_by_slug(self, organization_id: UUID, project_id: UUID, slug: str) -> Service | None:
        result = await self.session.execute(
            select(Service).where(
                Service.organization_id == organization_id,
                Service.project_id == project_id,
                Service.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def get_with_details(self, service_id: UUID) -> Service | None:
        result = await self.session.execute(
            select(Service)
            .options(
                selectinload(Service.project),
                selectinload(Service.environment),
            )
            .where(Service.id == service_id)
        )
        return result.scalar_one_or_none()

    async def count_by_project(self, project_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(Service.id)).where(Service.project_id == project_id)
        )
        return result.scalar_one()

    async def list_by_project(self, project_id: UUID, skip: int = 0, limit: int = 100) -> Sequence[Service]:
        result = await self.session.execute(
            select(Service)
            .where(Service.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

from uuid import UUID
from typing import Sequence
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.db.models.service_dependency import ServiceDependency

class DependencyRepository(BaseRepository[ServiceDependency]):
    def __init__(self, session):
        super().__init__(ServiceDependency, session)

    async def get_upstream_dependencies(self, service_id: UUID) -> Sequence[ServiceDependency]:
        result = await self.session.execute(
            select(ServiceDependency)
            .where(ServiceDependency.downstream_service_id == service_id)
        )
        return result.scalars().all()
        
    async def get_downstream_dependencies(self, service_id: UUID) -> Sequence[ServiceDependency]:
        result = await self.session.execute(
            select(ServiceDependency)
            .where(ServiceDependency.upstream_service_id == service_id)
        )
        return result.scalars().all()

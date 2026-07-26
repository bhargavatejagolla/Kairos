from uuid import UUID
from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.db.models.incident import Incident

class IncidentRepository(BaseRepository[Incident]):
    def __init__(self, session):
        super().__init__(Incident, session)

    async def get_by_number(self, organization_id: UUID, number: str) -> Incident | None:
        result = await self.session.execute(
            select(Incident)
            .options(selectinload(Incident.service))
            .where(
                Incident.organization_id == organization_id,
                Incident.number == number
            )
        )
        return result.scalar_one_or_none()

    async def count_by_service(self, service_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(Incident.id)).where(Incident.service_id == service_id)
        )
        return result.scalar_one()

    async def list_by_service(self, service_id: UUID, skip: int = 0, limit: int = 100) -> Sequence[Incident]:
        result = await self.session.execute(
            select(Incident)
            .where(Incident.service_id == service_id)
            .order_by(Incident.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.alert_policy import AlertPolicy
from app.repositories.base import BaseRepository

class AlertPolicyRepository(BaseRepository[AlertPolicy]):
    def __init__(self, session: AsyncSession):
        super().__init__(AlertPolicy, session)

    async def list_by_project(self, project_id: UUID) -> Sequence[AlertPolicy]:
        stmt = select(AlertPolicy).where(AlertPolicy.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

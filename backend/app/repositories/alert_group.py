from typing import Sequence, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.alert_group import AlertGroup
from app.repositories.base import BaseRepository

class AlertGroupRepository(BaseRepository[AlertGroup]):
    def __init__(self, session: AsyncSession):
        super().__init__(AlertGroup, session)

    async def get_by_correlation_key(self, organization_id: UUID, correlation_key: str, status: str = "OPEN") -> Optional[AlertGroup]:
        stmt = select(AlertGroup).where(
            AlertGroup.organization_id == organization_id,
            AlertGroup.correlation_key == correlation_key,
            AlertGroup.status == status
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def list_by_organization(self, organization_id: UUID, skip: int = 0, limit: int = 100) -> Sequence[AlertGroup]:
        stmt = select(AlertGroup).where(AlertGroup.organization_id == organization_id).order_by(AlertGroup.opened_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

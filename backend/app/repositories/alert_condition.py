from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert_condition import AlertCondition
from app.repositories.base import BaseRepository


class AlertConditionRepository(BaseRepository[AlertCondition]):
    def __init__(self, session: AsyncSession):
        super().__init__(AlertCondition, session)

    async def list_by_definition(self, definition_id: UUID) -> Sequence[AlertCondition]:
        stmt = select(AlertCondition).where(AlertCondition.definition_id == definition_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

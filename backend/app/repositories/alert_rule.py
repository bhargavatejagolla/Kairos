from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.alert_rule import AlertRule
from app.db.models.enums import RuleStatus
from app.repositories.base import BaseRepository

class AlertRuleRepository(BaseRepository[AlertRule]):
    def __init__(self, session: AsyncSession):
        super().__init__(AlertRule, session)

    async def get_active_rules(self) -> Sequence[AlertRule]:
        stmt = (
            select(AlertRule)
            .options(selectinload(AlertRule.definitions))
            .where(AlertRule.enabled == True, AlertRule.status == RuleStatus.ACTIVE)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_service(self, service_id: UUID, skip: int = 0, limit: int = 100) -> Sequence[AlertRule]:
        stmt = select(AlertRule).where(AlertRule.service_id == service_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.escalation_policy import EscalationPolicy
from app.repositories.base import BaseRepository


class EscalationPolicyRepository(BaseRepository[EscalationPolicy]):
    def __init__(self, session: AsyncSession):
        super().__init__(EscalationPolicy, session)

    async def list_by_organization(self, organization_id: UUID) -> Sequence[EscalationPolicy]:
        stmt = select(EscalationPolicy).where(EscalationPolicy.organization_id == organization_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

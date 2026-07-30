from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.signal import Signal
from app.repositories.base import BaseRepository


class SignalRepository(BaseRepository[Signal]):
    def __init__(self, session: AsyncSession):
        super().__init__(Signal, session)

    async def list_by_service(self, service_id: UUID, skip: int = 0, limit: int = 100) -> Sequence[Signal]:
        stmt = select(Signal).where(Signal.service_id == service_id).order_by(Signal.received_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

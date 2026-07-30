from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.silence import Silence
from app.repositories.base import BaseRepository


class SilenceRepository(BaseRepository[Silence]):
    def __init__(self, session: AsyncSession):
        super().__init__(Silence, session)

    async def get_active_silences(self, service_id: UUID, current_time: datetime) -> Sequence[Silence]:
        stmt = select(Silence).where(
            Silence.service_id == service_id,
            Silence.starts_at <= current_time,
            Silence.ends_at >= current_time
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

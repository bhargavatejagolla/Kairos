from typing import Sequence
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.maintenance_window import MaintenanceWindow
from app.repositories.base import BaseRepository

class MaintenanceWindowRepository(BaseRepository[MaintenanceWindow]):
    def __init__(self, session: AsyncSession):
        super().__init__(MaintenanceWindow, session)

    async def get_active_windows(self, service_id: UUID, current_time: datetime) -> Sequence[MaintenanceWindow]:
        # For simplicity, ignoring recurrence in this basic DB query stub
        stmt = select(MaintenanceWindow).where(
            MaintenanceWindow.service_id == service_id,
            MaintenanceWindow.starts_at <= current_time,
            MaintenanceWindow.ends_at >= current_time
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

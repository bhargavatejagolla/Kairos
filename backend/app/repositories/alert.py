from typing import Sequence, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.alert import Alert
from app.db.models.enums import AlertStatus
from app.repositories.base import BaseRepository

class AlertRepository(BaseRepository[Alert]):
    def __init__(self, session: AsyncSession):
        super().__init__(Alert, session)

    async def get_by_fingerprint(self, fingerprint: str, status: AlertStatus = AlertStatus.OPEN) -> Optional[Alert]:
        stmt = select(Alert).where(Alert.fingerprint == fingerprint, Alert.status == status)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def list_by_service(self, service_id: UUID, skip: int = 0, limit: int = 100) -> Sequence[Alert]:
        stmt = select(Alert).where(Alert.service_id == service_id).order_by(Alert.triggered_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

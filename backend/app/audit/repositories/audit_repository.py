from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Optional

from app.audit.models.audit_log import AuditLog
from app.audit.models.actor import AuditActor
from app.audit.models.target import AuditTarget
from app.audit.models.change import AuditChange
from app.audit.models.metadata import AuditMetadata

class AuditRepository:
    """
    Persistence-only layer for Audit.
    Strictly enforced Immutability: NO update() or delete() methods exist here.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, audit_log: AuditLog) -> AuditLog:
        self.session.add(audit_log)
        await self.session.flush()
        return audit_log

    async def get_by_id(self, log_id: UUID) -> Optional[AuditLog]:
        stmt = select(AuditLog).where(AuditLog.id == log_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_correlation_id(self, correlation_id: str) -> List[AuditLog]:
        stmt = select(AuditLog).where(AuditLog.correlation_id == correlation_id).order_by(AuditLog.created_at)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

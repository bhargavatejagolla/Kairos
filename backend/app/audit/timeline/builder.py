from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID

from app.audit.models.audit_log import AuditLog
from app.audit.models.actor import AuditActor
from app.audit.models.target import AuditTarget

class TimelineBuilder:
    """
    Unified Timeline Engine.
    Builds a chronological timeline of events for any resource, user, project, or correlation ID.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_correlation_id(self, correlation_id: str) -> List[AuditLog]:
        stmt = (
            select(AuditLog)
            .options(
                selectinload(AuditLog.actor),
                selectinload(AuditLog.targets),
                selectinload(AuditLog.changes),
                selectinload(AuditLog.metadata_info)
            )
            .where(AuditLog.correlation_id == correlation_id)
            .order_by(AuditLog.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_resource_id(self, resource_id: str) -> List[AuditLog]:
        """
        Builds a timeline for a specific resource (Incident, Alert, etc.)
        It finds any audit log where this resource is a target.
        """
        stmt = (
            select(AuditLog)
            .join(AuditTarget, AuditLog.id == AuditTarget.audit_log_id)
            .options(
                selectinload(AuditLog.actor),
                selectinload(AuditLog.targets),
                selectinload(AuditLog.changes),
                selectinload(AuditLog.metadata_info)
            )
            .where(AuditTarget.resource_id == resource_id)
            .order_by(AuditLog.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_actor_id(self, actor_id: str) -> List[AuditLog]:
        """
        Builds a timeline of all actions taken by a specific user or system actor.
        """
        stmt = (
            select(AuditLog)
            .join(AuditActor, AuditLog.id == AuditActor.audit_log_id)
            .options(
                selectinload(AuditLog.actor),
                selectinload(AuditLog.targets),
                selectinload(AuditLog.changes),
                selectinload(AuditLog.metadata_info)
            )
            .where(AuditActor.actor_id == actor_id)
            .order_by(AuditLog.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_project_id(self, project_id: UUID) -> List[AuditLog]:
        """
        Builds a timeline of all activity within a specific project.
        """
        stmt = (
            select(AuditLog)
            .options(
                selectinload(AuditLog.actor),
                selectinload(AuditLog.targets),
                selectinload(AuditLog.changes),
                selectinload(AuditLog.metadata_info)
            )
            .where(AuditLog.project_id == project_id)
            .order_by(AuditLog.created_at.desc()) # Note: Usually project view is desc
            .limit(100)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

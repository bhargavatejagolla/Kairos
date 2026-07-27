from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any, List
from datetime import datetime, timedelta, UTC
from uuid import UUID

from app.audit.models.audit_log import AuditLog
from app.audit.models.actor import AuditActor

class AuditAnalyticsEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_activity_summary(self, organization_id: UUID, days: int = 7) -> Dict[str, Any]:
        """
        Returns a high-level summary of activity for the dashboard.
        """
        since = datetime.now(UTC) - timedelta(days=days)
        
        # Total events
        stmt_total = select(func.count()).where(
            AuditLog.organization_id == organization_id,
            AuditLog.created_at >= since
        )
        total_events = (await self.session.execute(stmt_total)).scalar()
        
        # Group by severity
        stmt_severity = select(AuditLog.severity, func.count()).where(
            AuditLog.organization_id == organization_id,
            AuditLog.created_at >= since
        ).group_by(AuditLog.severity)
        severity_counts = dict((await self.session.execute(stmt_severity)).all())
        
        return {
            "total_events": total_events,
            "severity_distribution": {s.value: c for s, c in severity_counts.items()},
            "period_days": days
        }

    async def get_most_active_users(self, organization_id: UUID, days: int = 7, limit: int = 5) -> List[Dict[str, Any]]:
        since = datetime.now(UTC) - timedelta(days=days)
        
        stmt = (
            select(AuditActor.actor_id, AuditActor.actor_email, func.count())
            .join(AuditLog, AuditLog.id == AuditActor.audit_log_id)
            .where(
                AuditLog.organization_id == organization_id,
                AuditLog.created_at >= since,
                AuditActor.actor_type == "USER"
            )
            .group_by(AuditActor.actor_id, AuditActor.actor_email)
            .order_by(func.count().desc())
            .limit(limit)
        )
        
        results = await self.session.execute(stmt)
        return [{"actor_id": r[0], "email": r[1], "event_count": r[2]} for r in results.all()]

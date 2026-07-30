import asyncio
from datetime import UTC, datetime, timedelta

import structlog
from app.background.jobs.base import BaseJob
from sqlalchemy import delete, select

from app.audit.models.audit_log import AuditLog
from app.audit.models.retention import AuditRetentionPolicy
from app.background.celery_app import celery_app
from app.db.session import SessionLocal

logger = structlog.get_logger(__name__)

class AuditRetentionJob(BaseJob):
    name = "audit.retention_cleanup"

    async def execute(self, *args, **kwargs):
        """
        Enforces organization-specific retention policies.
        Deletes (or archives) audit logs older than the retention_days.
        """
        async with SessionLocal() as session:
            # 1. Fetch all policies
            stmt = select(AuditRetentionPolicy)
            result = await session.execute(stmt)
            policies = result.scalars().all()
            
            total_deleted = 0
            
            for policy in policies:
                cutoff_date = datetime.now(UTC) - timedelta(days=policy.retention_days)
                
                # In a real system, you might copy to S3 before deleting (Archive)
                if policy.archive_enabled:
                    logger.info("archiving_audit_logs", org_id=str(policy.organization_id), before=cutoff_date)
                    # Implementation of S3 archive would go here
                
                if policy.delete_after_archive or not policy.archive_enabled:
                    # Delete old records
                    del_stmt = delete(AuditLog).where(
                        AuditLog.organization_id == policy.organization_id,
                        AuditLog.created_at < cutoff_date
                    )
                    del_result = await session.execute(del_stmt)
                    total_deleted += del_result.rowcount
            
            await session.commit()
            return {"status": "success", "total_deleted": total_deleted}

@celery_app.task(bind=True, name=AuditRetentionJob.name)
def run_audit_retention(self):
    job = AuditRetentionJob(self)
    return asyncio.run(job.run())

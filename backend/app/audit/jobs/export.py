from app.background.celery_app import celery_app
from app.background.jobs.base import BaseJob
from app.db.session import SessionLocal
from app.audit.models.export import AuditExport
from app.audit.search.search_engine import AuditSearchEngine
from sqlalchemy import select
import structlog
import asyncio
import csv
import json
import os
from uuid import UUID
from datetime import datetime, UTC

logger = structlog.get_logger(__name__)

class AuditExportJob(BaseJob):
    name = "audit.export_generator"

    async def execute(self, export_id: str, *args, **kwargs):
        """
        Background job to generate an audit export file.
        """
        async with SessionLocal() as session:
            stmt = select(AuditExport).where(AuditExport.id == UUID(export_id))
            result = await session.execute(stmt)
            export_record = result.scalars().first()
            
            if not export_record:
                logger.error("export_record_not_found", export_id=export_id)
                return {"status": "error"}
                
            export_record.status = "PROCESSING"
            await session.commit()
            
            try:
                # 1. Reconstruct Search Query
                # In a real app, the search filters would be stored in AuditExport or passed in kwargs
                # For this MVP, we fetch the recent logs for the org
                search_engine = AuditSearchEngine(session)
                filters = {"organization_id": str(export_record.organization_id)}
                
                # Using page_size=10000 for a bulk export
                items, _ = await search_engine.search(filters, page=1, page_size=10000)
                
                # 2. Write to file
                export_dir = "/tmp/kairos_exports"
                os.makedirs(export_dir, exist_ok=True)
                file_path = f"{export_dir}/export_{export_id}.{export_record.format.lower()}"
                
                if export_record.format == "CSV":
                    with open(file_path, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(["ID", "Timestamp", "Event Type", "Action", "Severity", "Actor ID"])
                        for item in items:
                            actor_id = item.actor.actor_id if item.actor else ""
                            writer.writerow([item.id, item.created_at.isoformat(), item.event_type, item.action.value, item.severity.value, actor_id])
                elif export_record.format == "JSON":
                    data = []
                    for item in items:
                        data.append({
                            "id": str(item.id),
                            "timestamp": item.created_at.isoformat(),
                            "event_type": item.event_type,
                            "action": item.action.value,
                            "severity": item.severity.value
                        })
                    with open(file_path, "w") as f:
                        json.dump(data, f)
                
                export_record.file_path = file_path
                export_record.status = "COMPLETED"
                export_record.completed_at = datetime.now(UTC)
                await session.commit()
                
                logger.info("audit_export_completed", export_id=export_id, format=export_record.format)
                return {"status": "success", "file": file_path}
                
            except Exception as e:
                logger.error("audit_export_failed", export_id=export_id, error=str(e))
                export_record.status = "FAILED"
                await session.commit()
                raise e

@celery_app.task(bind=True, name=AuditExportJob.name)
def run_audit_export(self, export_id: str):
    job = AuditExportJob(self)
    return asyncio.run(job.run(export_id))

from app.background.celery_app import celery_app
from app.background.jobs.base import BaseJob
from app.db.session import SessionLocal
from app.events.outbox_service import OutboxService
import structlog
import asyncio

logger = structlog.get_logger(__name__)

class ProcessOutboxJob(BaseJob):
    name = "events.process_outbox"

    async def execute(self, *args, **kwargs):
        async with SessionLocal() as session:
            outbox_service = OutboxService(session)
            await outbox_service.publish_pending_events()
            return {"status": "success"}

@celery_app.task(bind=True, name=ProcessOutboxJob.name)
def process_outbox_task(self):
    job = ProcessOutboxJob(self)
    return asyncio.run(job.run())

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, UTC
import structlog
import uuid

from app.events.models import EventOutbox
from app.events.schema import DomainEvent
from app.events.bus import event_bus

logger = structlog.get_logger(__name__)

class OutboxService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_event(self, event: DomainEvent):
        """
        Save event to outbox within the same business transaction.
        """
        outbox_entry = EventOutbox(
            id=uuid.UUID(event.event_id),
            event_type=event.event_type,
            payload=event.model_dump(mode="json"),
            correlation_id=event.correlation_id,
            published=False
        )
        self.session.add(outbox_entry)
        # We do NOT commit here. The caller commits the transaction.

    async def publish_pending_events(self, batch_size: int = 100):
        """
        Finds unpublished events, publishes them to the in-memory bus, and marks them published.
        In a multi-worker setup, this should use SELECT FOR UPDATE SKIP LOCKED.
        """
        stmt = select(EventOutbox).where(EventOutbox.published == False).limit(batch_size).with_for_update(skip_locked=True)
        result = await self.session.execute(stmt)
        events = result.scalars().all()

        if not events:
            return

        for outbox_entry in events:
            try:
                # Dispatch to internal memory bus
                # Subscribers like Audit and Notifications will handle it from there
                event_bus.publish(outbox_entry.event_type, outbox_entry.payload)
                
                # Also publish to wildcard "Audit.Event" so Audit can record everything
                event_bus.publish("Audit.Event", outbox_entry.payload)
                
                outbox_entry.published = True
                outbox_entry.published_at = datetime.now(UTC)
                
            except Exception as e:
                logger.error("outbox_publish_failed", event_id=str(outbox_entry.id), error=str(e))
                # Leave published=False so it retries later

        await self.session.commit()

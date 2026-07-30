import structlog

from app.audit.schemas.audit import AuditEventCreate
from app.audit.services.audit_service import AuditService
from app.db.session import SessionLocal
from app.events.bus import EventBus

logger = structlog.get_logger(__name__)

async def handle_audit_event(event_data: dict):
    """
    Subscribes to 'Audit.Event' and creates an immutable audit log.
    """
    try:
        event = AuditEventCreate(**event_data)
        async with SessionLocal() as session:
            service = AuditService(session)
            await service.create_audit_record(event)
    except Exception as e:
        logger.error("audit_event_handling_failed", error=str(e), payload=event_data)

def register_audit_events(bus: EventBus):
    bus.subscribe("Audit.Event", handle_audit_event)
    logger.info("audit_events_registered")

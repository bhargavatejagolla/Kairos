import structlog

from app.db.session import SessionLocal
from app.events.bus import EventBus
from app.notifications.routing.notification_router import NotificationRouter

logger = structlog.get_logger(__name__)

async def route_event(event_type: str, event_data: dict):
    async with SessionLocal() as session:
        router = NotificationRouter(session)
        await router.dispatch_event(event_type, event_data)

async def handle_incident_created(event_data: dict):
    await route_event("IncidentCreated", event_data)
    
async def handle_alert_triggered(event_data: dict):
    await route_event("AlertTriggered", event_data)
    
async def handle_user_registered(event_data: dict):
    await route_event("UserRegistered", event_data)

def register_notification_events(bus: EventBus):
    bus.subscribe("IncidentCreated", handle_incident_created)
    bus.subscribe("AlertTriggered", handle_alert_triggered)
    bus.subscribe("UserRegistered", handle_user_registered)
    logger.info("notification_events_registered")

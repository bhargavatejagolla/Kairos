from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.events.bus import event_bus
from app.notifications.events.notification_events import register_notification_events
from app.audit.events.audit_events import register_audit_events
from app.core.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    Handles resource initialization and cleanup.
    """
    configure_logging()

    # Startup
    logger.info("Starting up application")
    register_notification_events(event_bus)
    register_audit_events(event_bus)

    logger.info(
        "application_started",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )

    yield

    import app.main as main_app
    import asyncio
    
    logger.info("Initiating graceful shutdown...")
    # 1. Mark readiness probe as failed so K8s stops sending new traffic
    main_app.is_shutting_down = True
    
    # 2. Wait for current requests to finish (Kubernetes grace period buffer)
    await asyncio.sleep(5)
    
    logger.info(
        "application_shutdown",
        application=settings.app_name,
    )

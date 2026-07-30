from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.audit.events.audit_events import register_audit_events
from app.core.config import settings
from app.core.logging import configure_logging, logger
from app.events.bus import event_bus
from app.notifications.events.notification_events import register_notification_events
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


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
    
    # Initialize Rate Limiter & Cache
    redis_conn = redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)
    FastAPICache.init(RedisBackend(redis_conn), prefix="kairos-cache")

    yield

    import asyncio

    import app.main as main_app
    
    logger.info("Initiating graceful shutdown...")
    # 1. Mark readiness probe as failed so K8s stops sending new traffic
    main_app.is_shutting_down = True
    
    # 2. Wait for current requests to finish (Kubernetes grace period buffer)
    await asyncio.sleep(5)
    
    logger.info(
        "application_shutdown",
        application=settings.app_name,
    )

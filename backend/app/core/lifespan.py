from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()

    logger.info(
        "application_started",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )

    yield

    logger.info(
        "application_shutdown",
        application=settings.app_name,
    )

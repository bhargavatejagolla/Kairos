import logging
import sys

import structlog

from app.core.config import settings


def configure_logging() -> None:
    # 1. Standard processors for all environments
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # 2. Environment-aware rendering
    if settings.app_env == "production":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    # 3. Configure structlog
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 4. Intercept standard library logging (Uvicorn, FastAPI, SQLAlchemy)
    # This forces standard logs through the structlog pipeline
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )
    
    for _log in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "sqlalchemy.engine.Engine"]:
        std_logger = logging.getLogger(_log)
        std_logger.handlers = [logging.StreamHandler(sys.stdout)]
        std_logger.propagate = False

logger = structlog.get_logger()

import logging
import sys

import structlog

from app.core.config import settings


def configure_logging() -> None:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ]

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        stream=sys.stdout,
        format="%(message)s",
    )

    structlog.configure(
        processors=processors,  # type: ignore[arg-type]
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()

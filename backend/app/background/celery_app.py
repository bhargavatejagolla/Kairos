from celery import Celery

from .config import background_config
from .queues import CELERY_QUEUES
from .routing import CELERY_ROUTES

celery_app = Celery(
    "kairos_background",
    broker=background_config.CELERY_BROKER_URL,
    backend=background_config.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_queues=CELERY_QUEUES,
    task_routes=CELERY_ROUTES,
    task_default_queue=background_config.TASK_DEFAULT_QUEUE,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_time_limit=background_config.TASK_HARD_TIMEOUT,
    task_soft_time_limit=background_config.TASK_SOFT_TIMEOUT,
)

# Autodiscover tasks from all standard modules
celery_app.autodiscover_tasks(['app.background', 'app.notifications', 'app.events', 'app.audit'])

import uuid

import structlog
from celery.signals import task_postrun, task_prerun

# Instrument Celery for OpenTelemetry
from opentelemetry.instrumentation.celery import CeleryInstrumentor

from app.middleware.correlation import correlation_id_var

CeleryInstrumentor().instrument()

@task_prerun.connect
def setup_structlog_context(task_id, task, *args, **kwargs):
    # Try to extract correlation_id from kwargs, or generate a new one
    req_kwargs = kwargs.get('kwargs', {})
    correlation_id = req_kwargs.get('correlation_id') or str(uuid.uuid4())
    
    correlation_id_var.set(correlation_id)
    structlog.contextvars.bind_contextvars(
        correlation_id=correlation_id,
        celery_task_id=task_id,
        celery_task_name=task.name
    )

@task_postrun.connect
def teardown_structlog_context(*args, **kwargs):
    structlog.contextvars.clear_contextvars()


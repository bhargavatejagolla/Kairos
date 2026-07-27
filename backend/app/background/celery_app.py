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
celery_app.autodiscover_tasks(['app.background'])

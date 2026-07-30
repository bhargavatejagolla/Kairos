from app.core.config import settings


class BackgroundConfig:
    CELERY_BROKER_URL = settings.celery_broker_url
    CELERY_RESULT_BACKEND = settings.celery_result_backend
    TASK_DEFAULT_QUEUE = "default"
    TASK_RETRY_LIMIT = 3
    TASK_RETRY_DELAY = 5
    TASK_HARD_TIMEOUT = 300
    TASK_SOFT_TIMEOUT = 240
    
background_config = BackgroundConfig()

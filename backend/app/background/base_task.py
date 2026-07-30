import logging

import celery

from .config import background_config

logger = logging.getLogger(__name__)

class BaseTask(celery.Task):
    """
    Base celery task providing DB sessions, contextual logging, 
    and exponential backoff retries.
    """
    abstract = True
    max_retries = background_config.TASK_RETRY_LIMIT
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {self.name}[{task_id}] failed: {exc}")
        # Custom logic for DLQ handling could be injected here
        super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {self.name}[{task_id}] succeeded.")
        super().on_success(retval, task_id, args, kwargs)
        
    def get_retry_delay(self, request):
        """Exponential backoff: 5, 10, 20, 40..."""
        retries = request.retries
        return background_config.TASK_RETRY_DELAY * (2 ** retries)

import logging

from celery.signals import worker_ready

from .events import TaskEventMonitor

logger = logging.getLogger(__name__)

@worker_ready.connect
def setup_worker(sender, **kwargs):
    logger.info("Worker is ready! Initializing dependencies...")
    sender.app.steps['worker'].add(TaskEventMonitor)

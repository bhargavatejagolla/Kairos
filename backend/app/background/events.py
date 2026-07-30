import logging

from celery import bootsteps

logger = logging.getLogger(__name__)

class TaskEventMonitor(bootsteps.StartStopStep):
    """Monitors task events and forwards them to the Event Bus (future)."""
    requires = ('celery.worker.components:Timer',)

    def __init__(self, worker, **kwargs):
        logger.info("Initializing Task Event Monitor")
        
    def start(self, worker):
        logger.info("Task Event Monitor started")

    def stop(self, worker):
        logger.info("Task Event Monitor stopped")

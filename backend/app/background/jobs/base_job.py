from app.background.base_task import BaseTask
from app.background.monitoring.logging import get_job_logger
from app.background.monitoring.metrics import record_job_metrics
from app.background.monitoring.tracing import trace_job
from app.background.reliability.distributed_lock import distributed_lock


class BaseJob(BaseTask):
    """
    Enterprise Base Job with idempotency, locks, tracing, metrics, and structured logging.
    """
    abstract = True

    def validate_idempotency(self, idempotency_key: str) -> bool:
        # We will acquire a lock here and if another worker holds it, it raises
        return True
        
    def __call__(self, *args, **kwargs):
        logger = get_job_logger(self.name, kwargs.get('request_id'))
        logger.info(f"Starting {self.name}")
        
        # OpenTelemetry Trace
        @trace_job(self.name)
        def _execute():
            # Apply Distributed Lock
            lock_key = kwargs.get('idempotency_key') or self.request.id
            with distributed_lock(lock_key):
                # Execute Celery Task
                result = super(BaseJob, self).__call__(*args, **kwargs)
                return result
                
        try:
            res = _execute()
            record_job_metrics(self.queue, "success")
            logger.info(f"Finished {self.name}")
            return res
        except Exception as e:
            record_job_metrics(self.queue, "failed")
            logger.error(f"Failed {self.name}: {e}")
            raise

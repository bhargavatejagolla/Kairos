from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob


@celery_app.task(bind=True, base=BaseJob)
def cleanup_cache(self):
    return {"status": "cleaned"}

@celery_app.task(bind=True, base=BaseJob)
def daily_report(self):
    return {"status": "reported"}

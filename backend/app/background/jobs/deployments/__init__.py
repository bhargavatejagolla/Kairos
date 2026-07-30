from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob


@celery_app.task(bind=True, base=BaseJob)
def github_sync(self):
    return {"status": "synced"}

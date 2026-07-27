from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob

@celery_app.task(bind=True, base=BaseJob)
def send_slack(self, message: str):
    return {"status": "sent"}

@celery_app.task(bind=True, base=BaseJob)
def send_email(self, message: str):
    return {"status": "sent"}

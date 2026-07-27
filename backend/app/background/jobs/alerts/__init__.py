from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob

@celery_app.task(bind=True, base=BaseJob)
def alert_analysis(self, alert_id: str):
    return {"status": "analyzed"}

@celery_app.task(bind=True, base=BaseJob)
def alert_escalation(self, alert_id: str):
    return {"status": "escalated"}

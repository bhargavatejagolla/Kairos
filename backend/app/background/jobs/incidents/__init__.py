from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob

@celery_app.task(bind=True, base=BaseJob)
def sla_monitor(self):
    return {"status": "sla_checked"}

@celery_app.task(bind=True, base=BaseJob)
def archive_incident(self, incident_id: str):
    return {"status": "archived"}

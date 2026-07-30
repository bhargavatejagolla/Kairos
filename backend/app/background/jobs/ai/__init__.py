from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob


@celery_app.task(bind=True, base=BaseJob)
def analyze_incident(self, incident_id: str, idempotency_key: str = None):
    if idempotency_key and not self.validate_idempotency(idempotency_key):
        return {"status": "duplicate", "incident_id": incident_id}
    return {"status": "analyzing", "incident_id": incident_id}

@celery_app.task(bind=True, base=BaseJob)
def summary(self, incident_id: str):
    return {"status": "summarized", "incident_id": incident_id}

@celery_app.task(bind=True, base=BaseJob)
def recommendation(self, incident_id: str):
    return {"status": "recommended", "incident_id": incident_id}

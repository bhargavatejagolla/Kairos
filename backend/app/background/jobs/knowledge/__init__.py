from app.background.celery_app import celery_app
from app.background.jobs.base_job import BaseJob


@celery_app.task(bind=True, base=BaseJob)
def chunk_document(self, document_id: str):
    return {"status": "chunked"}

@celery_app.task(bind=True, base=BaseJob)
def embed_document(self, document_id: str):
    return {"status": "embedded"}

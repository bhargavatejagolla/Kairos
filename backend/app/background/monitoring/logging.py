import structlog

# Initialize base structured logger
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20), # INFO
)

def get_job_logger(job_name: str, request_id: str = None, organization_id: str = None, worker_id: str = None):
    logger = structlog.get_logger(
        job_name=job_name,
        request_id=request_id,
        organization_id=organization_id,
        worker=worker_id
    )
    return logger

from prometheus_client import Counter, Histogram

# General Job Metrics
JOB_TOTAL = Counter('background_jobs_total', 'Total number of background jobs', ['queue', 'status'])
JOB_DURATION = Histogram('background_jobs_duration_seconds', 'Duration of jobs', ['queue'])
JOB_RETRIES = Counter('background_retries_total', 'Total number of retries', ['queue'])

# AI Specific Metrics
AI_JOBS = Counter('ai_jobs_total', 'Total AI specific jobs run', ['job_name'])
AI_FAILURES = Counter('ai_provider_failures', 'Failures interfacing with AI providers', ['provider'])

def record_job_metrics(queue: str, status: str, duration: float = 0.0):
    JOB_TOTAL.labels(queue=queue, status=status).inc()
    if duration > 0:
        JOB_DURATION.labels(queue=queue).observe(duration)

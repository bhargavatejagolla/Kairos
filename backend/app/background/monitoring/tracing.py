from opentelemetry import trace
from functools import wraps

tracer = trace.get_tracer("kairos.background")

def trace_job(job_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(job_name) as span:
                span.set_attribute("job.name", job_name)
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("job.status", "success")
                    return result
                except Exception as e:
                    span.set_attribute("job.status", "failed")
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator

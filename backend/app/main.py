from fastapi import FastAPI, Request
from prometheus_client import make_asgi_app
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import time

from app.api.exception_handlers import register_exception_handlers
from app.api.v1 import auth, organizations, permissions, ping, projects, roles, users
from app.container.application import container
from app.core.lifespan import lifespan
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.correlation import CorrelationIdMiddleware
from app.core.metrics import http_requests_total, http_request_duration_seconds
from app.core.tracing import configure_tracing

# Configure tracing for the application
configure_tracing()

app = FastAPI(
    title=container.settings.app_name,
    version=container.settings.app_version,
    description="AI-Powered DevOps Incident Intelligence Platform",
    lifespan=lifespan,
)

# Instrument FastAPI for distributed tracing
FastAPIInstrumentor.instrument_app(app)

# Metrics Middleware
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Avoid tracking the metrics endpoint itself
    if request.url.path != "/metrics":
        http_requests_total.labels(
            method=request.method, 
            endpoint=request.url.path, 
            status=response.status_code
        ).inc()
        http_request_duration_seconds.labels(
            method=request.method, 
            endpoint=request.url.path
        ).observe(duration)
        
    return response

# Prometheus Exporter Endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(CorrelationIdMiddleware)
register_exception_handlers(app)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to KAIROS API"}


# Kubernetes Probes
import asyncio

# A simple flag to determine if the app is shutting down
is_shutting_down = False

@app.get("/live", tags=["Health"])
async def live() -> dict[str, str]:
    """Liveness probe: Determines if the container is running and not deadlocked."""
    return {"status": "ok"}

@app.get("/ready", tags=["Health"])
async def ready() -> dict[str, str]:
    """Readiness probe: Determines if the app is ready to accept traffic."""
    if is_shutting_down:
        from fastapi import Response, status
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content="Shutting down")
    # In a real app, you might check DB connection here
    return {"status": "ok"}

@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    """General health endpoint for external monitoring."""
    return {"status": "ok", "version": container.settings.app_version}


app.include_router(ping.router, prefix="/api/v1", tags=["Ping"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(
    permissions.router, prefix="/api/v1/permissions", tags=["Permissions"]
)
app.include_router(
    organizations.router, prefix="/api/v1",
)
app.include_router(
    projects.router, prefix="/api/v1/organizations/{slug}/projects", tags=["Projects"]
)

# Phase 14: Enterprise Audit Platform
from app.api.v1.audit import router as audit_router
app.include_router(audit_router, prefix="/api/v1/audit")

# AI Routes
from app.api.ai import (
    chat_router,
    incident_router,
    alert_router,
    knowledge_router,
    prompt_router,
    conversation_router,
)

app.include_router(chat_router, prefix="/api/v1/ai/chat", tags=["AI Chat"])
app.include_router(incident_router, prefix="/api/v1/ai/incidents", tags=["AI Incidents"])
app.include_router(alert_router, prefix="/api/v1/ai/alerts", tags=["AI Alerts"])
app.include_router(knowledge_router, prefix="/api/v1/knowledge", tags=["AI Knowledge"])
app.include_router(prompt_router, prefix="/api/v1/prompts", tags=["AI Prompts"])
app.include_router(conversation_router, prefix="/api/v1/ai/conversations", tags=["AI Conversations"])


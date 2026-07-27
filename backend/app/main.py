from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.v1 import auth, organizations, permissions, ping, projects, roles, users
from app.container.application import container
from app.core.lifespan import lifespan
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.correlation import CorrelationIdMiddleware

app = FastAPI(
    title=container.settings.app_name,
    version=container.settings.app_version,
    description="AI-Powered DevOps Incident Intelligence Platform",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(CorrelationIdMiddleware)
register_exception_handlers(app)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to KAIROS API"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


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


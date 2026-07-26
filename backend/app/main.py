from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.v1 import auth, organizations, permissions, ping, projects, roles, users
from app.container.application import container
from app.core.lifespan import lifespan
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(
    title=container.settings.app_name,
    version=container.settings.app_version,
    description="AI-Powered DevOps Incident Intelligence Platform",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
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

from fastapi import FastAPI

from app.api.v1 import ping
from app.container.application import container
from app.core.handlers import register_exception_handlers
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
async def root():
    return {
        "message": "Welcome to KAIROS API"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


app.include_router(
    ping.router,
    prefix="/api/v1",
    tags=["Ping"]
)
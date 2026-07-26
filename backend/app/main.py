from fastapi import FastAPI

from app.api.v1 import ping
from app.core.config import settings
from app.core.lifespan import lifespan

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered DevOps Incident Intelligence Platform",
    lifespan=lifespan,
)


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
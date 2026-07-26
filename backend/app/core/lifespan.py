from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 50)
    print(f"Starting {settings.app_name}")
    print(f"Environment : {settings.app_env}")
    print(f"Version      : {settings.app_version}")
    print("=" * 50)

    yield

    print("=" * 50)
    print(f"Shutting down {settings.app_name}")
    print("=" * 50)

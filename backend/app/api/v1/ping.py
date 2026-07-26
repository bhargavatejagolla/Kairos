from fastapi import APIRouter

from app.services.ping_service import ping_service

router = APIRouter()


@router.get("/ping")
async def ping():
    return ping_service.ping()

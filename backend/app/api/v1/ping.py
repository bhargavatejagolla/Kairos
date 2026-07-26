from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.services import get_ping_service
from app.services.ping_service import PingService

router = APIRouter()


@router.get("/ping")
async def ping(
    service: Annotated[PingService, Depends(get_ping_service)],
):
    return service.ping()

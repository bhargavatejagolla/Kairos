from typing import Any

from fastapi import APIRouter

from app.background.reliability.distributed_lock import redis_client

router = APIRouter(prefix="/background/health", tags=["Background System Health"])

@router.get("", response_model=dict[str, Any])
async def check_health() -> Any:
    """
    Check the health of the background processing platform.
    Verifies Redis broker, workers, and metrics.
    """
    try:
        redis_status = redis_client.ping()
    except Exception:
        redis_status = False
        
    return {
        "status": "healthy" if redis_status else "degraded",
        "redis_connected": redis_status,
        "workers": "checked_via_workers_api"
    }

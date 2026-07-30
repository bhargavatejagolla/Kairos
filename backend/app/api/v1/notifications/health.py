import socket

from fastapi import APIRouter

from app.notifications.config.smtp import smtp_config

router = APIRouter(prefix="/health", tags=["Notification Health"])

@router.get("")
async def check_health():
    """
    Check SMTP connectivity and general notification subsystem health.
    """
    health = {
        "status": "up",
        "smtp_configured": bool(smtp_config.host and smtp_config.user),
        "smtp_host": smtp_config.host,
        "smtp_reachable": False
    }

    try:
        # Simple socket connection to verify SMTP port is open
        socket.create_connection((smtp_config.host, smtp_config.port), timeout=2)
        health["smtp_reachable"] = True
    except Exception as e:
        health["status"] = "degraded"
        health["error"] = str(e)
        
    return health

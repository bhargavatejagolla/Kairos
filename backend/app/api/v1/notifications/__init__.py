from fastapi import APIRouter

from .notifications import router as notifications_router
from .templates import router as templates_router
from .preferences import router as preferences_router
from .health import router as health_router

router = APIRouter()

router.include_router(notifications_router)
router.include_router(templates_router)
router.include_router(preferences_router)
router.include_router(health_router)

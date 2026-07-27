from fastapi import APIRouter
from app.api.v1.background.tasks import router as tasks_router
from app.api.v1.background.health import router as health_router
from app.api.v1.background.workers import router as workers_router

router = APIRouter()
router.include_router(tasks_router)
router.include_router(health_router)
router.include_router(workers_router)

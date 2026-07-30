from fastapi import APIRouter

from app.api.v1.audit.analytics import router as analytics_router
from app.api.v1.audit.exports import router as exports_router
from app.api.v1.audit.investigations import router as investigations_router
from app.api.v1.audit.search import router as search_router
from app.api.v1.audit.timeline import router as timeline_router

router = APIRouter()

router.include_router(search_router, tags=["Audit Search"])
router.include_router(timeline_router, prefix="/timeline", tags=["Audit Timeline"])
router.include_router(analytics_router, prefix="/analytics", tags=["Audit Analytics"])
router.include_router(investigations_router, prefix="/investigations", tags=["Audit Investigations"])
router.include_router(exports_router, prefix="/exports", tags=["Audit Exports"])

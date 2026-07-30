from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_user
from app.api.deps.database import get_db
from app.audit.investigations.profiles import SavedInvestigationProfiles
from app.audit.schemas.audit import AuditLogResponse
from app.audit.search.search_engine import AuditSearchEngine
from app.db.models.user import User

router = APIRouter()

@router.post("/search", response_model=list[AuditLogResponse])
async def search_audit_logs(
    filters: dict[str, Any],
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search audit logs across the organization.
    """
    search_engine = AuditSearchEngine(db)
    
    # Enforce organization isolation if applicable
    # filters["organization_id"] = str(current_user.organization_id)
    
    items, total = await search_engine.search(filters, page=page, page_size=page_size)
    return items

@router.get("/filters")
async def get_saved_filters(
    current_user: User = Depends(get_current_user)
):
    """
    Returns available saved investigation profiles.
    """
    return SavedInvestigationProfiles.list_profiles()

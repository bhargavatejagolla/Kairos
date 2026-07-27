from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from app.api.deps.auth import get_current_user
from app.api.deps.database import get_db
from app.db.models.user import User

from app.audit.search.search_engine import AuditSearchEngine
from app.audit.investigations.profiles import SavedInvestigationProfiles
from app.audit.schemas.audit import AuditLogResponse

router = APIRouter()

@router.get("/profiles")
async def get_profiles(current_user: User = Depends(get_current_user)):
    """
    List all available saved investigation profiles.
    """
    return SavedInvestigationProfiles.list_profiles()

@router.post("/profiles/{profile_id}/execute", response_model=List[AuditLogResponse])
async def execute_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Execute a saved investigation profile.
    """
    profile = SavedInvestigationProfiles.get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    filters = dict(profile["filters"])
    filters["organization_id"] = str(current_user.organization_id)
    
    search_engine = AuditSearchEngine(db)
    items, _ = await search_engine.search(filters, page=1, page_size=100)
    
    return items

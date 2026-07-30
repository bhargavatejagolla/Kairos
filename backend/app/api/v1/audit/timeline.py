
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_user
from app.api.deps.database import get_db
from app.audit.investigations.correlation import CorrelationWorkspace
from app.audit.schemas.audit import AuditLogResponse
from app.audit.timeline.builder import TimelineBuilder
from app.db.models.user import User

router = APIRouter()

@router.get("/resource/{resource_id}", response_model=list[AuditLogResponse])
async def get_resource_timeline(
    resource_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns the timeline for a specific resource (Incident, Alert, AI, etc.)
    """
    builder = TimelineBuilder(db)
    timeline = await builder.get_by_resource_id(resource_id)
    return timeline

@router.get("/correlation/{correlation_id}")
async def get_correlation_timeline(
    correlation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns a cross-domain investigation trace for a specific correlation ID.
    """
    workspace = CorrelationWorkspace(db)
    trace = await workspace.build_investigation_trace(correlation_id)
    
    if not trace["timeline"]:
        raise HTTPException(status_code=404, detail="Correlation ID not found")
        
    return trace

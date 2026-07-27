from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Dict, Any

from app.api.deps.auth import get_current_user
from app.api.deps.database import get_db
from app.db.models.user import User

from app.audit.models.export import AuditExport
from app.background.celery_app import celery_app

router = APIRouter()

class ExportRequest(BaseModel):
    format: str = "CSV" # CSV or JSON
    filters: Dict[str, Any] = {}

@router.post("")
async def create_export(
    request: ExportRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers a background job to export audit logs.
    """
    export = AuditExport(
        organization_id=current_user.organization_id,
        requested_by_id=current_user.id,
        status="PENDING",
        format=request.format
    )
    db.add(export)
    await db.commit()
    await db.refresh(export)
    
    # Trigger celery task
    celery_app.send_task(
        "audit.export_generator",
        args=[str(export.id)],
        queue="default"
    )
    
    return {"message": "Export job queued", "export_id": export.id}

@router.get("/{export_id}")
async def get_export_status(
    export_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check the status of an export job.
    """
    export = await db.get(AuditExport, export_id)
    if not export or export.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Export not found")
        
    return {
        "id": export.id,
        "status": export.status,
        "format": export.format,
        "created_at": export.created_at,
        "completed_at": export.completed_at,
        "file_path": export.file_path if export.status == "COMPLETED" else None
    }

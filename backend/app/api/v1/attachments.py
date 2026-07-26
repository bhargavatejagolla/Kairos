from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.api.deps.incident import IncidentDep
from app.api.deps.authorization import require_incident_permission
from app.core.permissions import Permission
from app.core.command_bus import command_bus

router = APIRouter(tags=["Attachments"])

@router.post(
    "/incidents/{incident_number}/attachments",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_UPDATE))]
)
async def upload_attachment(
    incident: IncidentDep
):
    # Dummy implementation
    return {"message": "Attachment uploaded"}

@router.get(
    "/incidents/{incident_number}/attachments",
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_VIEW))]
)
async def list_attachments(
    incident: IncidentDep
):
    # Dummy implementation
    return []

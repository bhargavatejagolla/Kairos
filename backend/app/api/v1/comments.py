
from fastapi import APIRouter, Depends, status

from app.api.deps.authorization import require_incident_permission
from app.api.deps.incident import IncidentDep
from app.core.permissions import Permission

router = APIRouter(tags=["Comments"])

@router.post(
    "/incidents/{incident_number}/comments",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_UPDATE))]
)
async def create_comment(
    incident: IncidentDep
):
    # Dummy implementation
    return {"message": "Comment created"}

@router.get(
    "/incidents/{incident_number}/comments",
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_VIEW))]
)
async def list_comments(
    incident: IncidentDep
):
    # Dummy implementation
    return []

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.authorization import require_incident_permission
from app.api.deps.incident import IncidentDep
from app.api.deps.services import get_timeline_service
from app.core.permissions import Permission
from app.schemas.timeline import TimelineEntryResponse
from app.services.timeline_service import TimelineService

router = APIRouter(tags=["Timelines"])

@router.get(
    "/incidents/{incident_number}/timeline",
    response_model=list[TimelineEntryResponse],
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_VIEW))]
)
async def get_incident_timeline(
    incident: IncidentDep,
    timeline_service: Annotated[TimelineService, Depends(get_timeline_service)]
):
    return await timeline_service.list_by_incident(incident.id)

from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.deps.service import ServiceContextDep
from app.api.deps.search import IncidentSearchDep
from app.api.deps.authorization import require_service_permission
from app.core.permissions import Permission
from app.schemas.statistics import IncidentStatistics

router = APIRouter(tags=["Statistics"])

@router.get(
    "/organizations/{org_slug}/projects/{project_slug}/services/{service_slug}/statistics",
    response_model=IncidentStatistics,
    dependencies=[Depends(require_service_permission(Permission.INCIDENTS_VIEW))]
)
async def get_statistics(
    ctx: ServiceContextDep,
    search: IncidentSearchDep
):
    # Dummy implementation for now, should call a statistics service
    return IncidentStatistics(
        total_incidents=10,
        open_incidents=2,
        resolved_incidents=8,
        by_severity={"SEV_1": 1, "SEV_3": 9},
        by_status={"OPEN": 2, "RESOLVED": 8},
        mttr_minutes=120,
        mtta_minutes=5
    )

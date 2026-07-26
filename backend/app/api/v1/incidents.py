from fastapi import APIRouter, Depends, status, Path
from typing import Annotated

from app.api.deps.service import ServiceContextDep
from app.api.deps.incident import IncidentDep
from app.api.deps.search import IncidentSearchDep
from app.api.deps.pagination import PaginationParams
from app.api.deps.authorization import require_incident_permission
from app.api.deps.hardening import get_idempotency_key
from app.core.permissions import Permission
from app.core.command_bus import command_bus
from app.workflow.commands import (
    CreateIncidentCommand, 
    AcknowledgeIncidentCommand,
    ResolveIncidentCommand,
    MitigateIncidentCommand,
    CloseIncidentCommand,
    AssignIncidentCommand
)
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.schemas.pagination import PaginatedResponse
from app.api.deps.services import get_incident_service
from app.services.incident_service import IncidentService

router = APIRouter(tags=["Incidents"])

@router.post(
    "/organizations/{org_slug}/projects/{project_slug}/services/{service_slug}/incidents",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_CREATE))]
)
async def create_incident(
    data: IncidentCreate,
    ctx: ServiceContextDep,
    idempotency_key: Annotated[str | None, Depends(get_idempotency_key)]
):
    command = CreateIncidentCommand(
        service_id=ctx.service.id,
        organization_id=ctx.organization.id,
        project_id=ctx.project.id,
        title=data.title,
        description=data.description,
        severity=data.severity,
        priority=data.priority,
        source=data.source,
        actor_id=ctx.member.user_id
    )
    # The command bus will locate the CreateIncidentHandler and run it
    return await command_bus.execute(command)

@router.get(
    "/organizations/{org_slug}/projects/{project_slug}/services/{service_slug}/incidents",
    response_model=PaginatedResponse[IncidentResponse],
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_VIEW))]
)
async def list_incidents(
    ctx: ServiceContextDep,
    search: IncidentSearchDep,
    pagination: Annotated[PaginationParams, Depends()],
    incident_service: Annotated[IncidentService, Depends(get_incident_service)]
):
    # In a full enterprise app, searching would be a separate read-model querying Elasticsearch or complex DB query.
    # We will simulate the call through the repository or service.
    # Note: IncidentService doesn't have a search method yet, so we'll leave a simple response format.
    incidents = [] 
    return PaginatedResponse.create(incidents, len(incidents), pagination.page, pagination.page_size)

@router.get(
    "/incidents/{incident_number}",
    response_model=IncidentResponse,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_VIEW))]
)
async def get_incident(
    incident: IncidentDep
):
    return incident

@router.post(
    "/incidents/{incident_number}/acknowledge",
    response_model=IncidentResponse,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_UPDATE))]
)
async def acknowledge_incident(
    incident: IncidentDep,
    ctx: ServiceContextDep
):
    command = AcknowledgeIncidentCommand(
        incident_id=incident.id,
        actor_id=ctx.member.user_id
    )
    return await command_bus.execute(command)

@router.post(
    "/incidents/{incident_number}/mitigate",
    response_model=IncidentResponse,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_UPDATE))]
)
async def mitigate_incident(
    incident: IncidentDep,
    ctx: ServiceContextDep
):
    command = MitigateIncidentCommand(
        incident_id=incident.id,
        actor_id=ctx.member.user_id
    )
    return await command_bus.execute(command)

@router.post(
    "/incidents/{incident_number}/resolve",
    response_model=IncidentResponse,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_RESOLVE))]
)
async def resolve_incident(
    incident: IncidentDep,
    ctx: ServiceContextDep
):
    command = ResolveIncidentCommand(
        incident_id=incident.id,
        actor_id=ctx.member.user_id
    )
    return await command_bus.execute(command)

@router.post(
    "/incidents/{incident_number}/close",
    response_model=IncidentResponse,
    dependencies=[Depends(require_incident_permission(Permission.INCIDENTS_CLOSE))]
)
async def close_incident(
    incident: IncidentDep,
    ctx: ServiceContextDep
):
    command = CloseIncidentCommand(
        incident_id=incident.id,
        actor_id=ctx.member.user_id
    )
    return await command_bus.execute(command)

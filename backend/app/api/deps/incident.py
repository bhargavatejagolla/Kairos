from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.organization import get_organization_context
from app.api.deps.services import get_incident_service
from app.core.organization_context import OrganizationContext
from app.db.models.incident import Incident
from app.services.incident_service import IncidentService

async def get_incident(
    incident_number: str = Path(..., description="The readable number of the incident (e.g., INC-0001)"),
    org_ctx: OrganizationContext = Depends(get_organization_context),
    incident_service: IncidentService = Depends(get_incident_service),
) -> Incident:
    try:
        incident = await incident_service.repository.get_by_number(
            organization_id=org_ctx.organization.id,
            number=incident_number,
        )
    except Exception:
        incident = None

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return incident

IncidentDep = Annotated[Incident, Depends(get_incident)]

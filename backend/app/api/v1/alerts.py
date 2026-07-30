from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.alert import get_alert_context
from app.api.deps.database import get_db
from app.schemas.alert import AlertResponse
from app.workflow.alert_workflow import AlertWorkflow
from app.workflow.workflow_context import AlertContext

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: UUID,
    service_id: UUID, # In a real implementation we'd resolve alert->service dynamically
    db: AsyncSession = Depends(get_db),
    ctx: AlertContext = Depends(get_alert_context),
):
    """
    Acknowledge an open alert.
    """
    workflow = AlertWorkflow(db)
    return await workflow.acknowledge_alert(ctx, alert_id)

@router.post("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: UUID,
    service_id: UUID,
    db: AsyncSession = Depends(get_db),
    ctx: AlertContext = Depends(get_alert_context),
):
    """
    Resolve an open or acknowledged alert.
    """
    workflow = AlertWorkflow(db)
    return await workflow.resolve_alert(ctx, alert_id)

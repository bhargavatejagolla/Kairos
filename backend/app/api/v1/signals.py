
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.alert import get_alert_context
from app.api.deps.database import get_db
from app.schemas.signal import SignalIn, SignalOut
from app.workflow.alert_workflow import AlertWorkflow
from app.workflow.workflow_context import AlertContext

router = APIRouter(prefix="/services/{service_id}/signals", tags=["Signals"])

@router.post("", response_model=SignalOut, status_code=status.HTTP_201_CREATED)
async def ingest_signal(
    signal_data: SignalIn,
    db: AsyncSession = Depends(get_db),
    ctx: AlertContext = Depends(get_alert_context),
):
    """
    Ingest a single telemetry signal and evaluate it against alert rules.
    """
    workflow = AlertWorkflow(db)
    signal = await workflow.ingest_signal(ctx, signal_data)
    return signal

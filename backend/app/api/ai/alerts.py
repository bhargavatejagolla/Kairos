from fastapi import APIRouter
from app.ai.workflows.alert_workflow import AlertWorkflow

router = APIRouter()
alert_workflow = AlertWorkflow()

@router.post("/{alert_id}/explain")
async def explain_alert(alert_id: str):
    return await alert_workflow.explain(alert_id)

@router.post("/{alert_id}/noise")
async def noise(alert_id: str):
    return {"noise_score": 0.1, "is_noise": False}

@router.post("/{alert_id}/priority")
async def priority(alert_id: str):
    return {"priority": "P1"}

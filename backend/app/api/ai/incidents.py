from fastapi import APIRouter
from app.ai.workflows.incident_workflow import IncidentWorkflow
from app.schemas.ai.responses import RootCauseResponse, RecommendationResponse, SummaryResponse

router = APIRouter()
incident_workflow = IncidentWorkflow()

@router.post("/{incident_id}/analyze")
async def analyze_incident(incident_id: str):
    return await incident_workflow.analyze(incident_id)

@router.post("/{incident_id}/root-cause", response_model=RootCauseResponse)
async def root_cause(incident_id: str):
    res = await incident_workflow.analyze(incident_id)
    return res["root_cause"]

@router.post("/{incident_id}/recommendations", response_model=RecommendationResponse)
async def recommendations(incident_id: str):
    res = await incident_workflow.analyze(incident_id)
    return res["recommendations"]

@router.post("/{incident_id}/summary")
async def summary(incident_id: str):
    return {"summary": "Stub Summary"}

@router.get("/{incident_id}/similar")
async def similar(incident_id: str):
    return []

@router.post("/{incident_id}/risk")
async def risk(incident_id: str):
    return {"risk": "High"}

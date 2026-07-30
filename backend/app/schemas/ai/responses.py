from uuid import UUID

from pydantic import BaseModel


class RootCauseResponse(BaseModel):
    root_cause: str
    confidence: float
    evidence: list[str]
    affected_services: list[str]
    recommended_actions: list[str]
    references: list[str]

class RecommendationResponse(BaseModel):
    recommendations: list[str]

class SummaryResponse(BaseModel):
    summary: str
    impact: str
    actions_taken: list[str]
    current_status: str
    remaining_risk: str

class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: UUID
    reply: str

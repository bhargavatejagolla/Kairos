from typing import Any, Dict
from app.ai.agents.base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    @property
    def role(self) -> str:
        return "incident_summarizer"
        
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "summary": "Service outage resolved.",
            "impact": "High",
            "actions_taken": ["Scaled pods"],
            "current_status": "RESOLVED",
            "remaining_risk": "Low"
        }

from typing import Any, Dict
from app.ai.agents.root_cause_agent import RootCauseAgent
from app.ai.agents.recommendation_agent import RecommendationAgent

class IncidentWorkflow:
    def __init__(self):
        self.root_cause_agent = RootCauseAgent()
        self.recommendation_agent = RecommendationAgent()
        
    async def analyze(self, incident_id: str) -> Dict[str, Any]:
        context = {"incident_id": incident_id}
        
        # 1. Gather Root Cause
        root_cause_res = await self.root_cause_agent.run(context)
        
        # 2. Gather Recommendations
        rec_res = await self.recommendation_agent.run(context)
        
        # 3. Increment Metric
        from app.core.metrics import ai_resolutions_total
        ai_resolutions_total.labels(
            organization_id="unknown", # Would need DB lookup for real org ID
            action_type="incident_analysis"
        ).inc()
        
        return {
            "incident_id": incident_id,
            "root_cause": root_cause_res,
            "recommendations": rec_res
        }

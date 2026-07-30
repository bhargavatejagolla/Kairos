from typing import Any

from app.ai.agents.base_agent import BaseAgent


class RootCauseAgent(BaseAgent):
    @property
    def role(self) -> str:
        return "root_cause_analyst"
        
    async def run(self, context: dict[str, Any]) -> dict[str, Any]:
        incident_id = context.get("incident_id")
        
        # 1. Use tools to gather data
        if self.tool_registry.get_tool("incident_tool"):
            incident_data = await self.tool_registry.get_tool("incident_tool").execute(incident_id=incident_id)
        
        # 2. Analyze
        # Stub response matching schemas.ai.responses.RootCauseResponse
        return {
            "root_cause": "Database connection timeout due to high load.",
            "confidence": 0.85,
            "evidence": ["CPU spike at 10:00 AM", "DB timeout logs"],
            "affected_services": ["payment-api"],
            "recommended_actions": ["Scale up DB instances"],
            "references": ["Runbook: DB Scaling"]
        }

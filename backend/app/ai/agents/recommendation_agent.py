from typing import Any

from app.ai.agents.base_agent import BaseAgent


class RecommendationAgent(BaseAgent):
    @property
    def role(self) -> str:
        return "recommendation_analyst"
        
    async def run(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "recommendations": ["Restart service", "Increase memory limit"]
        }

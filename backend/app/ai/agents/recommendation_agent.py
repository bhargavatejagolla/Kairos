from typing import Any, Dict
from app.ai.agents.base_agent import BaseAgent

class RecommendationAgent(BaseAgent):
    @property
    def role(self) -> str:
        return "recommendation_analyst"
        
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "recommendations": ["Restart service", "Increase memory limit"]
        }

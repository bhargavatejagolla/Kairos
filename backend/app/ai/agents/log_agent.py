from typing import Any

from app.ai.agents.base_agent import BaseAgent


class LogAgent(BaseAgent):
    @property
    def role(self) -> str:
        return "log_analyst"
        
    async def run(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "insights": ["Connection timeout in line 45"]
        }

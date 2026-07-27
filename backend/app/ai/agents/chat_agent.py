from typing import Any, Dict
from app.ai.agents.base_agent import BaseAgent

class ChatAgent(BaseAgent):
    @property
    def role(self) -> str:
        return "sre_assistant"
        
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        message = context.get("message")
        
        # In a real system, the chat agent parses the intent and uses tools dynamically
        return {
            "reply": f"I received your message: {message}. I am an AI SRE Assistant."
        }

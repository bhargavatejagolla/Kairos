from typing import Any
from tenacity import retry, stop_after_attempt, wait_exponential

from app.ai.agents.chat_agent import ChatAgent


class SessionManager:
    def get_context(self, session_id: str) -> dict[str, Any]:
        return {"session_id": session_id}
        
    def save_context(self, session_id: str, context: dict[str, Any]):
        pass

class ChatWorkflow:
    def __init__(self):
        self.chat_agent = ChatAgent()
        self.session_manager = SessionManager()
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def chat(self, session_id: str, message: str) -> dict[str, Any]:
        context = self.session_manager.get_context(session_id)
        context["message"] = message
        
        reply = await self.chat_agent.run(context)
        
        self.session_manager.save_context(session_id, context)
        return reply

from typing import Any, Dict
from app.ai.agents.chat_agent import ChatAgent

class SessionManager:
    def get_context(self, session_id: str) -> Dict[str, Any]:
        return {"session_id": session_id}
        
    def save_context(self, session_id: str, context: Dict[str, Any]):
        pass

class ChatWorkflow:
    def __init__(self):
        self.chat_agent = ChatAgent()
        self.session_manager = SessionManager()
        
    async def chat(self, session_id: str, message: str) -> Dict[str, Any]:
        context = self.session_manager.get_context(session_id)
        context["message"] = message
        
        reply = await self.chat_agent.run(context)
        
        self.session_manager.save_context(session_id, context)
        return reply

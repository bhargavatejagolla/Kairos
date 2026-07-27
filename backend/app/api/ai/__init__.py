from app.api.ai.chat import router as chat_router
from app.api.ai.incidents import router as incident_router
from app.api.ai.alerts import router as alert_router
from app.api.ai.knowledge import router as knowledge_router
from app.api.ai.prompts import router as prompt_router
from app.api.ai.conversations import router as conversation_router

__all__ = [
    "chat_router",
    "incident_router",
    "alert_router",
    "knowledge_router",
    "prompt_router",
    "conversation_router",
]

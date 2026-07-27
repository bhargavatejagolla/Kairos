from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.workflows.chat_workflow import ChatWorkflow
from app.schemas.ai.responses import ChatRequest, ChatResponse

router = APIRouter()
chat_workflow = ChatWorkflow()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Pass to chat workflow
    reply = await chat_workflow.chat(str(request.conversation_id), request.message)
    return ChatResponse(conversation_id=request.conversation_id, reply=reply["reply"])

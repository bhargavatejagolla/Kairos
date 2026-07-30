from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.ai.workflows.chat_workflow import ChatWorkflow
from app.schemas.ai.responses import ChatRequest, ChatResponse

router = APIRouter()
chat_workflow = ChatWorkflow()

@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def chat(request: ChatRequest):
    # Pass to chat workflow
    reply = await chat_workflow.chat(str(request.conversation_id), request.message)
    return ChatResponse(conversation_id=request.conversation_id, reply=reply["reply"])

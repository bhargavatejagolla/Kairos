from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_conversations():
    return []

@router.post("/{conversation_id}/messages")
async def add_message(conversation_id: str):
    return {"status": "added"}

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    return {"status": "deleted"}

from fastapi import APIRouter

router = APIRouter()

@router.post("/documents")
async def upload_document():
    # Enqueue embedding job
    return {"status": "processing"}

@router.get("/documents")
async def list_documents():
    return []

@router.post("/search")
async def search_knowledge():
    return []

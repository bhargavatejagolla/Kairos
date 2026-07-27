from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PromptCreate(BaseModel):
    name: str
    system_prompt: str
    user_template: str

@router.get("/")
async def list_prompts():
    return []

@router.post("/")
async def create_prompt(prompt: PromptCreate):
    # Logic to never overwrite, create v+1
    return {"name": prompt.name, "version": 1}

@router.patch("/{prompt_id}")
async def update_prompt(prompt_id: str):
    # Increment version
    return {"status": "updated to v+1"}

import logging
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.providers.base import LLMProvider
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.key_manager import KeyManager

logger = logging.getLogger(__name__)

class ModelRouter:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.key_manager = KeyManager(db)
        
    async def get_provider(self, requested_provider: str = "groq") -> LLMProvider:
        if requested_provider == "groq":
            key_record = await self.key_manager.get_available_key("groq")
            if not key_record:
                logger.warning("No available Groq keys in DB. Falling back to env GROQ_API_KEY")
                api_key = os.environ.get("GROQ_API_KEY")
                if not api_key:
                    raise ValueError("No Groq API keys available")
            else:
                # In a real app we wouldn't store raw keys in DB, we'd lookup secret by key_name
                api_key = os.environ.get(key_record.key_name)
                if not api_key:
                    raise ValueError(f"Secret not found for key: {key_record.key_name}")
                    
            return GroqProvider(api_key=api_key)
            
        raise ValueError(f"Unsupported provider: {requested_provider}")


import groq

from app.ai.providers.base import LLMProvider


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = groq.AsyncGroq(api_key=api_key)
        self.model = "llama3-8b-8192" # Default
        
    async def generate(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            messages=messages,
            model=kwargs.get("model", self.model),
        )
        return response.choices[0].message.content
        
    async def stream(self, prompt: str, system_prompt: str | None = None, **kwargs):
        raise NotImplementedError("Streaming not yet implemented")
        
    async def health(self) -> bool:
        return True

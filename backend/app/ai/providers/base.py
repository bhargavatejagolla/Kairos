from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        pass
        
    @abstractmethod
    async def stream(self, prompt: str, system_prompt: str | None = None, **kwargs):
        pass
        
    @abstractmethod
    async def health(self) -> bool:
        pass

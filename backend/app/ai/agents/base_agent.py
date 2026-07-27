from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.tools.registry import ToolRegistry

class BaseAgent(ABC):
    def __init__(self, tool_registry: ToolRegistry | None = None):
        self.tool_registry = tool_registry or ToolRegistry()
        
    @property
    @abstractmethod
    def role(self) -> str:
        pass
        
    @abstractmethod
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

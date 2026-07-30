from collections.abc import Callable
from typing import Any


class WorkflowRegistry:
    _registry: dict[str, Callable] = {}
    
    @classmethod
    def register(cls, event_name: str, handler: Callable):
        cls._registry[event_name] = handler
        
    @classmethod
    def dispatch(cls, event_name: str, payload: Any):
        if event_name in cls._registry:
            cls._registry[event_name](payload)

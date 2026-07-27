from typing import Callable, Dict, Any

class WorkflowRegistry:
    _registry: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, event_name: str, handler: Callable):
        cls._registry[event_name] = handler
        
    @classmethod
    def dispatch(cls, event_name: str, payload: Any):
        if event_name in cls._registry:
            cls._registry[event_name](payload)

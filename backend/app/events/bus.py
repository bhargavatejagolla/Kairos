from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class EventBus:
    """
    In-memory pub-sub event bus.
    For cross-process, this should bridge to Redis Pub/Sub.
    """
    _subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_name: str, handler: Callable):
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []
        cls._subscribers[event_name].append(handler)
        logger.info(f"Subscribed to {event_name}")

    @classmethod
    def publish(cls, event_name: str, payload: Any):
        logger.info(f"Publishing event {event_name}")
        handlers = cls._subscribers.get(event_name, [])
        for handler in handlers:
            try:
                # Typically, the handler will just trigger a WorkflowEngine
                handler(payload)
            except Exception as e:
                logger.error(f"Error handling event {event_name}: {e}")

# Global instance
event_bus = EventBus()

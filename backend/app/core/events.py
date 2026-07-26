from typing import Any, Awaitable, Callable

EventHandler = Callable[[Any], Awaitable[None]]

class EventBus:
    """
    A simple async event bus for domain events.
    In a distributed system, this could be backed by Kafka, RabbitMQ, or Redis.
    For now, it's an in-memory pub/sub mechanism.
    """
    def __init__(self):
        self._subscribers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, event_data: Any):
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                # In production, these should be dispatched to background tasks
                # to avoid blocking the HTTP request
                await handler(event_data)


# Global event bus instance
event_bus = EventBus()

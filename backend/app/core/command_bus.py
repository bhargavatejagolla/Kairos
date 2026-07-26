from typing import TypeVar, Type, Dict, Any, Generic, Protocol
from pydantic import BaseModel

class Command(BaseModel):
    """Base class for all commands."""
    pass

C = TypeVar('C', bound=Command)
R = TypeVar('R')

class CommandHandler(Protocol, Generic[C, R]):
    async def handle(self, command: C) -> R:
        ...

class CommandBus:
    def __init__(self):
        self._handlers: Dict[Type[Command], Any] = {}

    def register(self, command_type: Type[Command], handler: Any) -> None:
        if command_type in self._handlers:
            raise ValueError(f"Handler already registered for command {command_type.__name__}")
        self._handlers[command_type] = handler

    async def execute(self, command: Command) -> Any:
        command_type = type(command)
        handler = self._handlers.get(command_type)
        if not handler:
            raise ValueError(f"No handler registered for command {command_type.__name__}")
        
        return await handler.handle(command)

# Global command bus instance for easy dependency injection
command_bus = CommandBus()

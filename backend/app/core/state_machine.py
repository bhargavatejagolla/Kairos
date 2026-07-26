from typing import Any, Callable, Dict, List, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession

StateT = TypeVar("StateT")
ContextT = TypeVar("ContextT")

class StateTransitionError(Exception):
    def __init__(self, current_state: Any, target_state: Any, reason: str = ""):
        self.current_state = current_state
        self.target_state = target_state
        super().__init__(f"Invalid transition from {current_state} to {target_state}. {reason}")

class StateMachine(Generic[StateT, ContextT]):
    """Generic State Machine to govern entity lifecycle transitions."""
    
    def __init__(self, allowed_transitions: Dict[StateT, List[StateT]]):
        self.allowed_transitions = allowed_transitions
        self.before_hooks: Dict[tuple[StateT, StateT], List[Callable]] = {}
        self.after_hooks: Dict[tuple[StateT, StateT], List[Callable]] = {}

    def add_hook(self, current: StateT, target: StateT, hook: Callable, phase: str = "after"):
        key = (current, target)
        if phase == "before":
            self.before_hooks.setdefault(key, []).append(hook)
        else:
            self.after_hooks.setdefault(key, []).append(hook)

    def validate_transition(self, current_state: StateT, target_state: StateT):
        if target_state not in self.allowed_transitions.get(current_state, []):
            raise StateTransitionError(current_state, target_state)

    async def execute_transition(self, context: ContextT, current_state: StateT, target_state: StateT, session: AsyncSession):
        self.validate_transition(current_state, target_state)
        
        key = (current_state, target_state)
        for hook in self.before_hooks.get(key, []):
            await hook(context, session)
            
        # The actual state change is expected to be performed by the caller,
        # but this executes the business logic surrounding it.
        
        for hook in self.after_hooks.get(key, []):
            await hook(context, session)

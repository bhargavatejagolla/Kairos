from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import event_bus

class WorkflowEngine:
    """
    Sits above the state machine to handle what happens BECAUSE a transition occurred.
    (e.g., triggers notifications, updates SLAs, dispatches domain events).
    """

    async def process_transition(
        self,
        entity_name: str,
        entity_id: str,
        current_state: Any,
        target_state: Any,
        session: AsyncSession,
        metadata: Dict[str, Any] = None
    ):
        """
        Orchestrate the side-effects of a successful state transition.
        """
        if not metadata:
            metadata = {}
            
        # 1. Publish Domain Event (e.g. IncidentStatusChanged, IncidentResolved)
        event_name = f"{entity_name}Transitioned"
        
        payload = {
            "entity_id": entity_id,
            "previous_state": str(current_state),
            "new_state": str(target_state),
            **metadata
        }
        await event_bus.publish(event_name, payload)
        
        # 1.5 Emit Structured Logs and Metrics
        import logging
        logger = logging.getLogger("kairos.workflow")
        logger.info(
            "Workflow transition executed", 
            extra={
                "event": f"{entity_name.lower()}_transitioned",
                f"{entity_name.lower()}_id": entity_id,
                "previous_state": str(current_state),
                "new_state": str(target_state)
            }
        )
        
        # In a real app we'd use prometheus_client here.
        # e.g., COUNTER_WORKFLOW_TRANSITIONS.labels(entity=entity_name, state=target_state).inc()

        
        # 2. Trigger SLAs or Timers if needed (Future)
        # 3. Queue Notification triggers (Future)
        # 4. Automations (Future)

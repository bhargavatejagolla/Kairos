from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from app.audit.timeline.builder import TimelineBuilder
from app.audit.models.audit_log import AuditLog

class CorrelationWorkspace:
    """
    Cross-Domain Investigation Workspace.
    Groups events from Incidents, Alerts, AI, Background Tasks, Notifications 
    into a single cohesive trace using the Correlation ID.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.timeline_builder = TimelineBuilder(session)

    async def build_investigation_trace(self, correlation_id: str) -> Dict[str, Any]:
        """
        Returns a structured trace of all activities sharing the same correlation_id.
        """
        timeline = await self.timeline_builder.get_by_correlation_id(correlation_id)
        
        # Categorize events for the workspace UI
        trace = {
            "correlation_id": correlation_id,
            "total_events": len(timeline),
            "duration_ms": 0,
            "modules_involved": set(),
            "timeline": []
        }
        
        if not timeline:
            return trace
            
        start_time = timeline[0].created_at
        end_time = timeline[-1].created_at
        trace["duration_ms"] = int((end_time - start_time).total_seconds() * 1000)
        
        for log in timeline:
            trace["modules_involved"].add(log.source.value)
            
            event_data = {
                "id": str(log.id),
                "timestamp": log.created_at.isoformat(),
                "source": log.source.value,
                "event_type": log.event_type,
                "action": log.action.value,
                "severity": log.severity.value,
                "actor": log.actor.actor_id if log.actor else None,
                "targets": [t.resource_id for t in log.targets]
            }
            trace["timeline"].append(event_data)
            
        # Convert set to list for JSON serialization
        trace["modules_involved"] = list(trace["modules_involved"])
        
        return trace

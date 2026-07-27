from typing import Dict, Any, List
from uuid import UUID

from app.audit.models.audit_log import AuditLog

class AuditReplayService:
    """
    Audit Replay Engine.
    Reconstructs the state of a resource at a specific point in time by replaying its AuditChange records.
    """
    
    def reconstruct_state(self, timeline: List[AuditLog], target_resource_id: str, until_log_id: UUID = None) -> Dict[str, Any]:
        """
        Given a chronological list of AuditLogs for a resource, this replays the changes
        to build a JSON representation of the resource's state.
        
        If until_log_id is provided, it stops replaying once it processes that log.
        """
        state: Dict[str, Any] = {}
        
        for log in timeline:
            # Look for changes pertaining to the target_resource_id
            # In a strict implementation, AuditChange might store resource_id if an event affects multiple,
            # but for our simple case, we assume the changes array maps to the primary resource.
            for change in log.changes:
                if change.new_value is not None:
                    state[change.field_name] = change.new_value
                elif change.new_value is None and change.old_value is not None:
                    # Field was deleted/cleared
                    if change.field_name in state:
                        del state[change.field_name]
                        
            if until_log_id and log.id == until_log_id:
                break
                
        return state

import json
from uuid import UUID

class ContextBuilder:
    def build_incident_context(self, incident_id: UUID) -> str:
        # Fetch incident, timeline, alerts, metrics, deployments
        return json.dumps({
            "incident_id": str(incident_id),
            "status": "INVESTIGATING",
            "timeline": []
        })

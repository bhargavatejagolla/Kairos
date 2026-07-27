from typing import Any, Dict
from app.ai.tools.base import BaseTool

class IncidentTool(BaseTool):
    @property
    def name(self) -> str:
        return "incident_tool"
        
    @property
    def description(self) -> str:
        return "Fetches details and timeline for a specific incident."
        
    async def execute(self, incident_id: str, **kwargs) -> Dict[str, Any]:
        # Stub implementation
        return {"incident_id": incident_id, "status": "INVESTIGATING", "timeline": []}

class AlertTool(BaseTool):
    @property
    def name(self) -> str:
        return "alert_tool"
        
    @property
    def description(self) -> str:
        return "Fetches details for a specific alert."
        
    async def execute(self, alert_id: str, **kwargs) -> Dict[str, Any]:
        return {"alert_id": alert_id, "status": "FIRING"}

class MetricsTool(BaseTool):
    @property
    def name(self) -> str:
        return "metrics_tool"
        
    @property
    def description(self) -> str:
        return "Fetches recent metrics for a given service."
        
    async def execute(self, service_id: str, **kwargs) -> Dict[str, Any]:
        return {"service_id": service_id, "cpu": "95%", "memory": "80%"}

class LogsTool(BaseTool):
    @property
    def name(self) -> str:
        return "logs_tool"
        
    @property
    def description(self) -> str:
        return "Fetches recent error logs for a service."
        
    async def execute(self, service_id: str, **kwargs) -> Dict[str, Any]:
        return {"service_id": service_id, "logs": ["[ERROR] Connection refused"]}

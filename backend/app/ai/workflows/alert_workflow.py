from typing import Any, Dict

class AlertWorkflow:
    def __init__(self):
        pass
        
    async def explain(self, alert_id: str) -> Dict[str, Any]:
        return {
            "alert_id": alert_id,
            "explanation": "CPU is high because of new deployment."
        }

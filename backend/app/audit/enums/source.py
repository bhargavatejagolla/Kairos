from enum import Enum

class AuditSource(str, Enum):
    API = "API"
    SYSTEM = "SYSTEM"
    BACKGROUND = "BACKGROUND"
    AI = "AI"
    SCHEDULER = "SCHEDULER"
    WORKER = "WORKER"

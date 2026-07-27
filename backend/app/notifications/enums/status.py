from enum import Enum

class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RENDERING = "RENDERING"
    SENDING = "SENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

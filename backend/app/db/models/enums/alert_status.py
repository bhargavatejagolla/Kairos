from enum import Enum


class AlertStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    SUPPRESSED = "SUPPRESSED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

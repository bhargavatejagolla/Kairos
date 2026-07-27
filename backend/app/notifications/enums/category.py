from enum import Enum

class NotificationCategory(str, Enum):
    SECURITY = "SECURITY"
    INCIDENT = "INCIDENT"
    ALERT = "ALERT"
    SYSTEM = "SYSTEM"
    USER = "USER"
    REPORT = "REPORT"

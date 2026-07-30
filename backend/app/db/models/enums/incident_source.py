from enum import Enum


class IncidentSource(str, Enum):
    MANUAL = "MANUAL"
    ALERT = "ALERT"
    AI = "AI"
    WEBHOOK = "WEBHOOK"
    API = "API"

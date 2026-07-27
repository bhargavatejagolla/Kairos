from enum import Enum

class SignalType(str, Enum):
    METRIC = "METRIC"
    LOG = "LOG"
    TRACE = "TRACE"
    HEALTH_CHECK = "HEALTH_CHECK"
    HEARTBEAT = "HEARTBEAT"
    WEBHOOK = "WEBHOOK"
    AI = "AI"
    EXTERNAL = "EXTERNAL"

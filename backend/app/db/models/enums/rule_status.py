from enum import Enum


class RuleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    MUTED = "MUTED"

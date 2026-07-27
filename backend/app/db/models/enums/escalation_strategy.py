from enum import Enum

class EscalationStrategy(str, Enum):
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"
    ON_CALL = "ON_CALL"
    ROUND_ROBIN = "ROUND_ROBIN"

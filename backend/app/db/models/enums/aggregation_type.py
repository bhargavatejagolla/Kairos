from enum import Enum


class AggregationType(str, Enum):
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"
    SUM = "SUM"
    COUNT = "COUNT"
    P95 = "P95"
    P99 = "P99"

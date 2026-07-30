from enum import Enum


class AlertOperator(str, Enum):
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="
    EQUAL = "=="
    NOT_EQUAL = "!="
    BETWEEN = "BETWEEN"
    CONTAINS = "CONTAINS"
    REGEX = "REGEX"

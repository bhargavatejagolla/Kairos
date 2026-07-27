from enum import Enum

class NotificationChannelType(str, Enum):
    EMAIL = "EMAIL"
    SLACK = "SLACK"
    MICROSOFT_TEAMS = "MICROSOFT_TEAMS"
    WEBHOOK = "WEBHOOK"
    PAGERDUTY = "PAGERDUTY"

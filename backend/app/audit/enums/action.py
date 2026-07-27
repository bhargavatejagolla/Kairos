from enum import Enum

class AuditAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    VIEW = "VIEW"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXECUTE = "EXECUTE"
    EXPORT = "EXPORT"
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"
    ASSIGN = "ASSIGN"
    RESOLVE = "RESOLVE"
    ACKNOWLEDGE = "ACKNOWLEDGE"
    ESCALATE = "ESCALATE"

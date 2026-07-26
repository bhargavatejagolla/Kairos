from enum import Enum

class DependencyType(str, Enum):
    SYNCHRONOUS = "SYNCHRONOUS"
    ASYNCHRONOUS = "ASYNCHRONOUS"
    DATABASE = "DATABASE"
    CACHE = "CACHE"
    EXTERNAL_API = "EXTERNAL_API"

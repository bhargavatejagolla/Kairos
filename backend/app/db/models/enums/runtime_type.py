from enum import Enum

class RuntimeType(str, Enum):
    PYTHON = "PYTHON"
    JAVA = "JAVA"
    NODE = "NODE"
    GO = "GO"
    RUST = "RUST"
    DOTNET = "DOTNET"
    UNKNOWN = "UNKNOWN"

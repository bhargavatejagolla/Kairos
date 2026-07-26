from app.services.ping_service import PingService


def get_ping_service() -> PingService:
    """
    Returns the PingService instance.

    Centralizing dependency creation here makes it easy
    to replace implementations during testing or future
    refactoring.
    """
    return PingService()

class PingService:
    """Business logic related to application health."""

    @staticmethod
    def ping() -> dict[str, str]:
        return {
            "message": "pong"
        }


ping_service = PingService()

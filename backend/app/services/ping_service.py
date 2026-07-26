class PingService:
    """Business logic for application health."""

    def ping(self) -> dict[str, str]:
        return {"message": "pong"}

from fastapi.testclient import TestClient

from app.api.deps.services import get_ping_service
from app.main import app
from app.services.ping_service import PingService

client = TestClient(app)


def test_ping_endpoint():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_dependency_override():
    class MockPingService(PingService):
        def ping(self) -> dict[str, str]:
            return {"message": "mocked_pong"}

    app.dependency_overrides[get_ping_service] = lambda: MockPingService()
    try:
        response = client.get("/api/v1/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "mocked_pong"}
    finally:
        app.dependency_overrides.clear()

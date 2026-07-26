from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_request_id_header_present():
    response = client.get("/health")
    assert response.status_code == 200
    assert "x-request-id" in response.headers
    request_id = response.headers["x-request-id"]
    assert len(request_id) > 0


def test_unique_request_ids():
    res1 = client.get("/health")
    res2 = client.get("/health")
    assert res1.headers["x-request-id"] != res2.headers["x-request-id"]

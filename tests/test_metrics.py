from fastapi.testclient import TestClient

from telathbot import app


def test_metrics_and_status():
    with TestClient(app) as client:
        response = client.get("/metrics")
        assert response.status_code == 200

        response = client.get("/health")
        assert response.status_code == 200

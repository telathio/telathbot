from telathbot import app
from fastapi.testclient import TestClient


def test_metrics_and_status():
    with TestClient(app) as client:
        response = client.get("/metrics")
        assert response.status_code == 200

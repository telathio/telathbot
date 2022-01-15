from telathbot import app
from fastapi.testclient import TestClient

def test_metrics_and_status():
    with TestClient(app) as client:
        response = client.get("/metrics")
        assert response.status_code == 200
        response = client.get("/control/environ")
        assert response.status_code == 200
        response = client.get("/control/health")
        assert response.status_code == 200
        response = client.get("/control/heartbeat")
        assert response.status_code == 200
        response = client.get("/control/version")
        assert response.status_code == 200

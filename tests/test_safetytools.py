from fastapi.testclient import TestClient

from telathbot import app


def test_safetytools():
    with TestClient(app) as client:
        response = client.get("/safetytools/red")
        assert response.status_code == 200

        response_contents = response.json()

        assert response_contents[0]["post_id"] == 1
        assert len(response_contents[0]["reaction_users"]) > 0

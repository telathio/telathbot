from fastapi.testclient import TestClient

from telathbot import app


def test_safetytools():
    with TestClient(app) as client:
        client.delete("/safetytools/uses/red")
        response = client.post("/safetytools/uses/red", json={})
        assert response.status_code == 200

        response_contents = response.json()
        assert len(response_contents) == 2
        assert response_contents[0]["post_id"] == 1
        assert len(response_contents[0]["reaction_users"]) > 0

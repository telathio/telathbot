from fastapi.testclient import TestClient

from telathbot import app


def test_safetytools():
    with TestClient(app) as client:
        response = client.get("/safetytools/uses/red")
        assert response.status_code == 200

        response_contents = response.json()
        assert len(response_contents) == 2
        assert response_contents[0]["post_id"] == 1
        assert len(response_contents[0]["reaction_users"]) > 0


def test_safetytools_filter():
    with TestClient(app) as client:
        response = client.get("/safetytools/uses/red?last_post_id=1")
        assert response.status_code == 200

        response_contents = response.json()
        assert len(response_contents) == 1
        assert response_contents[0]["post_id"] == 2
        assert len(response_contents[0]["reaction_users"]) > 0


def test_safetytools_save_and_notify():
    with TestClient(app) as client:
        response = client.get(
            "/safetytools/uses/red?last_post_id=1&notify=true&persist=true"
        )
        assert response.status_code == 200

        response_contents = response.json()
        assert len(response_contents) == 1
        assert response_contents[0]["post_id"] == 2
        assert len(response_contents[0]["reaction_users"]) > 0

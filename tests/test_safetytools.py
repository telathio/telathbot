from fastapi.testclient import TestClient

from telathbot import app


def test_safetytools():
    with TestClient(app) as client:
        delete_response = client.delete("/safetytools/uses/red")
        assert delete_response.status_code == 200

        post_response = client.post("/safetytools/uses/red", json={})
        assert post_response.status_code == 200

        post_response_contents = post_response.json()
        assert len(post_response_contents) == 2
        assert post_response_contents[0]["post_id"] == 1
        assert len(post_response_contents[0]["reaction_users"]) > 0

        notify_response = client.post("/safetytools/notify/red", json={})
        assert notify_response.status_code == 200

        notify_response_content = notify_response.json()
        assert len(notify_response_content) == 2
        assert notify_response_content[0]["notified"] == True

        # Test notifications are only sent once.
        notify_response = client.post("/safetytools/notify/red", json={})
        assert notify_response.status_code == 200

        notify_response_content = notify_response.json()
        assert not len(notify_response_content)

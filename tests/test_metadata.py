from fastapi.testclient import TestClient

from telathbot import app


def test_metadata():
    with TestClient(app) as client:
        response = client.get("/metadata")
        assert response.status_code == 200

        response_contents = response.json()
        assert response_contents["type"] == "metadata"
        assert type(response_contents["lastPostId"]) == int
        assert response_contents["lastPublicIp"]
        assert type(response_contents["lastPublicIp"]) == str

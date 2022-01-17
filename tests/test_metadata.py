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


def test_metadata_check_ip():
    with TestClient(app) as client:
        request_body = {"ip": "1.1.1.1"}

        response = client.post("/metadata/check/ip", json=request_body)
        assert response.status_code == 200

        response_contents = response.json()
        assert response_contents["changed"] == True

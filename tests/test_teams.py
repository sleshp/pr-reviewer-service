import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_team_and_get(override_get_session):
    body = {
        "team_name": "BackendTest",
        "members": [
            {"user_id": "u1", "username": "Alice", "is_active": True},
            {"user_id": "u2", "username": "Bob", "is_active": True},
        ],
    }

    r = client.post("/team/add", json=body)
    assert r.status_code == 201

    r2 = client.get("/team/get", params={"team_name": "BackendTest"})
    assert r2.status_code == 200
    assert r2.json()["team"]["team_name"] == "BackendTest"

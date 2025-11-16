import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


async def create_team(client):
    body = {
        "team_name": "BackendPR",
        "members": [
            {"user_id": "u1", "username": "Author", "is_active": True},
            {"user_id": "u2", "username": "Reviewer1", "is_active": True},
            {"user_id": "u3", "username": "Reviewer2", "is_active": True},
        ],
    }
    r = client.post("/team/add", json=body)
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_create_pr_assigns_reviewers(override_get_session):
    await create_team(client)

    body = {
        "pull_request_id": "pr1",
        "pull_request_name": "Feature A",
        "author_id": "u1",
    }
    r = client.post("/pullRequest/create", json=body)
    assert r.status_code == 201

    pr = r.json()["pr"]
    assert pr["status"] == "OPEN"
    assert 1 <= len(pr["assigned_reviewers"]) <= 2

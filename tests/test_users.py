import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_set_is_active_and_get_review(override_get_session):
    r = client.post("/team/add", json={
        "team_name": "BackendUsers",
        "members": [
            {"user_id": "u1", "username": "Author", "is_active": True},
            {"user_id": "u2", "username": "Reviewer", "is_active": True},
        ]
    })
    assert r.status_code == 201

    r = client.post("/pullRequest/create", json={
        "pull_request_id": "pr_user",
        "pull_request_name": "User Test",
        "author_id": "u1"
    })
    assert r.status_code == 201

    reviewer = r.json()["pr"]["assigned_reviewers"][0]

    r2 = client.get("/users/getReview", params={"user_id": reviewer})
    assert r2.status_code == 200

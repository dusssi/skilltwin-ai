"""Security tests: isolation, traversal, uploads, malformed input, limits."""

import os

import pytest

from app.api.middleware import reset_rate_limit
from app.config.settings import settings
from tests.conftest import minimal_pdf_bytes, register


def test_user_isolation_on_sessions(alice, bob, client):
    thread = client.post("/chat", headers=alice["headers"], json={"message": "secret"}).json()
    session_id = thread["session_id"]
    # Bob must not read Alice's session (404, no leak).
    response = client.get(f"/chat/sessions/{session_id}/messages", headers=bob["headers"])
    assert response.status_code == 404
    # Bob's twin is unaffected by Alice.
    assert client.get("/twin", headers=bob["headers"]).json()["skills"] == []


def test_user_isolation_on_roadmap_items(alice, bob, client):
    client.patch("/twin", headers=alice["headers"], json={"target_role": "AI Intern"})
    items = client.post("/roadmap/generate", headers=alice["headers"], json={}).json()["items"]
    response = client.patch(f"/roadmap/items/{items[0]['id']}", headers=bob["headers"],
                            json={"status": "completed"})
    assert response.status_code == 404


def test_upload_path_traversal_neutralized(alice, client, tmp_env):
    pdf = minimal_pdf_bytes(["Traversal Tester", "Python SQL"])
    response = client.post(
        "/resume/upload", headers=alice["headers"],
        files={"file": ("../../evil.pdf", pdf, "application/pdf")},
    )
    assert response.status_code == 201
    stored = response.json()["resume"]["filename_stored"]
    assert ".." not in stored and "/" not in stored
    assert os.path.exists(os.path.join(tmp_env["uploads"], stored))
    # Nothing escaped the upload dir.
    parent = os.path.dirname(tmp_env["uploads"])
    assert not os.path.exists(os.path.join(parent, "evil.pdf"))


def test_upload_rejects_non_pdf(alice, client):
    response = client.post(
        "/resume/upload", headers=alice["headers"],
        files={"file": ("notes.pdf", b"this is not a pdf" * 10, "application/pdf")},
    )
    assert response.status_code == 400


def test_upload_rejects_bad_extension(alice, client):
    pdf = minimal_pdf_bytes(["x"])
    response = client.post(
        "/resume/upload", headers=alice["headers"],
        files={"file": ("run.exe", pdf, "application/octet-stream")},
    )
    assert response.status_code == 400


def test_upload_rejects_oversized(alice, client, monkeypatch):
    monkeypatch.setattr(settings, "MAX_UPLOAD_MB", 0)
    pdf = minimal_pdf_bytes(["big file", "Python"])
    response = client.post(
        "/resume/upload", headers=alice["headers"],
        files={"file": ("big.pdf", pdf, "application/pdf")},
    )
    assert response.status_code == 413


def test_malicious_username_rejected(client):
    response = client.post("/auth/register",
                           json={"username": "../root", "password": "password123"})
    assert response.status_code == 422


def test_malformed_requests_do_not_crash(alice, client):
    assert client.post("/chat", headers=alice["headers"], json={}).status_code == 422
    assert client.patch("/roadmap/items/abc", headers=alice["headers"],
                        json={"status": "completed"}).status_code == 422
    assert client.patch("/roadmap/items/1", headers=alice["headers"],
                        json={"status": "explode"}).status_code == 422


def test_rate_limiting_enforced(client, monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT_ENABLED", True)
    monkeypatch.setattr(settings, "RATE_LIMIT_SENSITIVE_PER_MINUTE", 2)
    reset_rate_limit()
    try:
        register(client, "rate1")
        register(client, "rate2")
        response = client.post("/auth/register",
                               json={"username": "rate3", "password": "password123"})
        assert response.status_code == 429
        assert response.json()["error"]["code"] == "rate_limited"
    finally:
        reset_rate_limit()

"""API tests: auth lifecycle and error envelopes."""

from tests.conftest import register


def test_health_and_ready(client):
    assert client.get("/").status_code == 200
    health = client.get("/health").json()
    assert health["status"] == "ok"
    assert health["database_ready"] is True
    assert client.get("/ready").status_code == 200


def test_register_login_me_logout(client):
    data = register(client, "carol")
    headers = {"Authorization": f"Bearer {data['token']}"}
    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["user"]["username"] == "carol"

    login = client.post("/auth/login", json={"username": "carol", "password": "password123"})
    assert login.status_code == 200
    assert login.json()["token"]

    logout = client.post("/auth/logout", headers={"Authorization": f"Bearer {login.json()['token']}"})
    assert logout.status_code == 200
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {login.json()['token']}"}).status_code == 401


def test_duplicate_username_conflict(client):
    register(client, "dave")
    response = client.post("/auth/register", json={"username": "dave", "password": "password123"})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "conflict"


def test_wrong_password_unauthorized(client):
    register(client, "erin")
    response = client.post("/auth/login", json={"username": "erin", "password": "wrongpass1"})
    assert response.status_code == 401


def test_missing_token_unauthorized(client):
    response = client.get("/twin")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_validation_error_envelope(client):
    response = client.post("/auth/register", json={"username": "x", "password": "short"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"

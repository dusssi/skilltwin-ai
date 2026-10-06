"""API tests: personalized chat grounded in the Twin + memory."""

import app.api.routes.chat as chat_route
from tests.conftest import StubProvider


def test_chat_fallback_is_honest_and_personal(alice, client):
    client.patch("/twin", headers=alice["headers"],
                 json={"target_role": "AI Intern", "primary_goal": "Get an AI internship"})
    client.post("/twin/skills", headers=alice["headers"], json={"name": "Python", "level": 3})
    response = client.post("/chat", headers=alice["headers"],
                           json={"message": "What should I learn next?"})
    assert response.status_code == 200
    body = response.json()
    assert body["fallback"] is True  # no API key in tests
    assert "unavailable" in body["response"]
    assert "Get an AI internship" in body["response"]  # twin-derived, not generic
    assert body["session_id"]


def test_same_question_differs_per_user(alice, bob, client, monkeypatch):
    client.patch("/twin", headers=alice["headers"],
                 json={"target_role": "AI Intern", "primary_goal": "Become an ML engineer"})
    client.post("/twin/skills", headers=alice["headers"], json={"name": "Python", "level": 4})
    client.patch("/twin", headers=bob["headers"],
                 json={"target_role": "Frontend Developer", "primary_goal": "Become a React dev"})
    client.post("/twin/skills", headers=bob["headers"], json={"name": "React", "level": 2})

    monkeypatch.setattr(chat_route.chat_service, "provider", StubProvider(echo_prompt=True))
    question = "What should I focus on?"
    alice_answer = client.post("/chat", headers=alice["headers"],
                               json={"message": question}).json()["response"]
    bob_answer = client.post("/chat", headers=bob["headers"],
                             json={"message": question}).json()["response"]
    assert alice_answer != bob_answer
    assert "ML engineer" in alice_answer and "Python" in alice_answer
    assert "React dev" in bob_answer and "React" in bob_answer


def test_chat_learns_goal_and_skills(alice, client):
    response = client.post("/chat", headers=alice["headers"], json={
        "message": "My goal is to become a Data Analyst. I know SQL and Python."})
    assert response.status_code == 200
    updates = {u["type"] for u in response.json()["twin_updates"]}
    assert "goal" in updates
    twin = client.get("/twin", headers=alice["headers"]).json()
    assert "Data Analyst" in twin["profile"]["primary_goal"]
    names = {s["skill_name"] for s in twin["skills"]}
    assert {"SQL", "Python"} <= names


def test_chat_history_and_sessions(alice, client):
    first = client.post("/chat", headers=alice["headers"], json={"message": "Hello twin"}).json()
    second = client.post("/chat", headers=alice["headers"],
                         json={"message": "Follow up", "session_id": first["session_id"]}).json()
    assert second["session_id"] == first["session_id"]
    thread = client.get(f"/chat/sessions/{first['session_id']}/messages",
                        headers=alice["headers"]).json()
    assert len(thread["messages"]) == 4
    assert [m["role"] for m in thread["messages"]] == ["user", "assistant", "user", "assistant"]
    sessions = client.get("/chat/sessions", headers=alice["headers"]).json()["sessions"]
    assert len(sessions) == 1
    assert sessions[0]["summary"]  # auto summary present

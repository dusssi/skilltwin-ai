"""API tests: memory recall influencing chat + recommendations."""

import app.api.routes.chat as chat_route
from tests.conftest import StubProvider


def test_memory_recall_and_search(alice, client):
    created = client.post("/memory", headers=alice["headers"], json={
        "kind": "preference", "content": "Prefers evening study sessions", "importance": 8,
    })
    assert created.status_code == 201
    memories = client.get("/memory", headers=alice["headers"]).json()["memories"]
    assert any("evening" in m["content"] for m in memories)
    found = client.get("/memory", headers=alice["headers"],
                       params={"q": "evening study"}).json()["memories"]
    assert found and "evening" in found[0]["content"]
    missing = client.get("/memory", headers=alice["headers"],
                         params={"q": "zebra astrophysics"}).json()["memories"]
    assert missing == []


def test_memory_influences_chat_prompt(alice, client, monkeypatch):
    client.post("/memory", headers=alice["headers"], json={
        "kind": "fact", "content": "Alice completed the Python donating-project milestone",
        "importance": 9,
    })
    stub = StubProvider(echo_prompt=True)
    monkeypatch.setattr(chat_route.chat_service, "provider", stub)
    answer = client.post("/chat", headers=alice["headers"],
                         json={"message": "What do you remember about my milestone?"}).json()
    assert "donating-project" in answer["response"]


def test_events_recorded(alice, client):
    client.patch("/twin", headers=alice["headers"], json={"primary_goal": "X"})
    events = client.get("/memory/events", headers=alice["headers"]).json()["events"]
    assert any(e["event_type"] == "career_goal_changed" for e in events)


def test_recommendations_from_twin(alice, client):
    client.patch("/twin", headers=alice["headers"], json={"target_role": "AI Intern"})
    client.post("/twin/skills", headers=alice["headers"], json={"name": "Python", "level": 3})
    generated = client.post("/recommendations/generate", headers=alice["headers"]).json()
    assert len(generated["projects"]) == 3
    listed = client.get("/recommendations", headers=alice["headers"]).json()["recommendations"]
    assert len(listed) >= 6
    rec_id = listed[0]["id"]
    updated = client.patch(f"/recommendations/{rec_id}", headers=alice["headers"],
                           json={"status": "accepted"}).json()
    assert updated["status"] == "accepted"


def test_knowledge_search_threshold(alice, client):
    hit = client.get("/knowledge/search", headers=alice["headers"],
                     params={"q": "how to prepare for AI internship"}).json()
    assert hit["results"]
    miss = client.get("/knowledge/search", headers=alice["headers"],
                      params={"q": "quantum banana zebra"}).json()
    assert miss["results"] == []

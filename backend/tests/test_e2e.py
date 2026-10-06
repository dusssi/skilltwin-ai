"""End-to-end SkillTwin flow: register → goal → resume → gaps → roadmap
→ chat → progress → twin update → memory → restart persistence."""

import app.api.routes.chat as chat_route
from fastapi.testclient import TestClient
from tests.conftest import StubProvider, register

RESUME_TEXT = (
    "Riya Verma\nPython developer with Git, GitHub, SQL.\n"
    "Built ML prototypes with scikit-learn.\n"
    "Projects: Sentiment Analyzer (Python, NLP), Marks Dashboard (SQL).\n"
    "B.Tech 2023. github.com/riya"
)


def test_full_skilltwin_flow(client, tmp_env, monkeypatch):
    # 1. Create user + set career goal.
    data = register(client, "riya", display_name="Riya")
    headers = {"Authorization": f"Bearer {data['token']}"}
    twin = client.patch("/twin", headers=headers, json={
        "target_role": "AI Intern", "primary_goal": "Get an AI internship"}).json()
    assert twin["role_key"] == "ai_intern"

    # 2. Upload resume (as text) → Twin updated.
    analysis = client.post("/resume/analyze", headers=headers,
                           json={"resume_text": RESUME_TEXT}).json()
    assert len(analysis["twin_diff"]["skills_added"]) >= 4
    skills = {s["skill_name"]: s for s in
              client.get("/twin/skills", headers=headers).json()["skills"]}
    assert skills["Python"]["level"] >= 2
    assert skills["Python"]["evidence"], "proficiency must carry evidence"

    # 3. Personalized gaps.
    gaps = client.get("/twin/gaps", headers=headers).json()["gaps"]
    assert gaps and all(g["reason"] and g["recommended_action"] for g in gaps)

    # 4. Personalized roadmap.
    roadmap = client.post("/roadmap/generate", headers=headers, json={}).json()
    assert len(roadmap["items"]) >= 3
    assert roadmap["items"][0]["skill"] in {g["skill_name"] for g in gaps}

    # 5. Chat knows the user (stubbed LLM echoes the assembled prompt).
    monkeypatch.setattr(chat_route.chat_service, "provider", StubProvider(echo_prompt=True))
    chat = client.post("/chat", headers=headers,
                       json={"message": "How do I reach my goal?"}).json()
    assert "Get an AI internship" in chat["response"]
    assert "Python" in chat["response"]

    # 6. Complete a roadmap item → skill evidence + proficiency update.
    skill_item = next(i for i in roadmap["items"] if i["skill"])
    before = skills.get(skill_item["skill"], {}).get("level", 0)
    done = client.patch(f"/roadmap/items/{skill_item['id']}", headers=headers,
                        json={"status": "completed"}).json()
    assert done["item"]["status"] == "completed"
    if before == 0:
        assert done["twin_change"]["new_level"] >= 1

    # 7. Memory stored.
    events = client.get("/memory/events", headers=headers).json()["events"]
    types = {e["event_type"] for e in events}
    assert {"resume_uploaded", "roadmap_item_completed", "roadmap_generated"} <= types

    # 8. Simulated restart: brand-new app + client over the SAME db file.
    from app.api.main import create_app

    with TestClient(create_app()) as fresh:
        twin_after = fresh.get("/twin", headers=headers).json()
        assert twin_after["summary"]["skills_count"] >= 4
        roadmap_after = fresh.get("/roadmap", headers=headers).json()
        assert roadmap_after["progress"]["completed"] == 1
        sessions = fresh.get("/chat/sessions", headers=headers).json()["sessions"]
        assert len(sessions) == 1

    # 9. Ask again → still personalized after restart.
    with TestClient(create_app()) as fresh2:
        again = fresh2.post("/chat", headers=headers,
                            json={"message": "What is my next step?"}).json()
        assert "Get an AI internship" in again["response"]

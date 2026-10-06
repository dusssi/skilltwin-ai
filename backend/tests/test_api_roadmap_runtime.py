"""API tests: roadmap generation/progress and the agent runtime."""

RESUME_TEXT = (
    "Sam. Python and Git user. Learning machine learning. BCA student. "
    "Project: Calculator app."
)


def _seed(alice, client):
    client.patch("/twin", headers=alice["headers"],
                 json={"target_role": "AI Intern", "primary_goal": "Get an AI internship"})
    client.post("/resume/analyze", headers=alice["headers"], json={"resume_text": RESUME_TEXT})


def test_roadmap_personalized_from_gaps(alice, client):
    _seed(alice, client)
    response = client.post("/roadmap/generate", headers=alice["headers"], json={})
    assert response.status_code == 201
    body = response.json()
    items = body["items"]
    assert len(items) >= 3
    first = items[0]
    assert {"title", "description", "skill", "difficulty", "estimated_effort",
            "priority", "status", "resources"} <= set(first)
    assert first["skill"]  # tied to a real gap skill
    assert first["status"] == "pending"
    assert body["progress"]["total"] == len(items)


def test_complete_item_updates_twin(alice, client):
    _seed(alice, client)
    items = client.post("/roadmap/generate", headers=alice["headers"], json={}).json()["items"]
    skill_item = next(item for item in items if item["skill"])
    before = {s["skill_name"]: s["level"] for s in
              client.get("/twin/skills", headers=alice["headers"]).json()["skills"]}
    done = client.patch(f"/roadmap/items/{skill_item['id']}", headers=alice["headers"],
                        json={"status": "completed"}).json()
    assert done["item"]["status"] == "completed"
    change = done["twin_change"]
    assert change["skill"] == skill_item["skill"]
    assert change["new_level"] >= before.get(skill_item["skill"], 0)
    active = client.get("/roadmap", headers=alice["headers"]).json()
    assert active["progress"]["completed"] == 1


def test_unknown_item_404(alice, client):
    assert client.patch("/roadmap/items/99999", headers=alice["headers"],
                        json={"status": "completed"}).status_code == 404


def test_runtime_run_completes(alice, client):
    _seed(alice, client)
    response = client.post("/runtime", headers=alice["headers"], json={"goal": "AI internship"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    result = body["result"]
    assert result["goal"] == "AI internship"
    assert len(result["observations"]) >= 5
    assert result["plan"]["steps"]
    assert "reflect" in result["completed_steps"]
    assert result["reflection"]["score"] >= 0
    assert result["summary"]


def test_runtime_bootstraps_empty_twin(alice, client):
    body = client.post("/runtime", headers=alice["headers"], json={}).json()
    assert body["status"] == "completed"
    assert "bootstrap_twin" in body["result"]["completed_steps"]

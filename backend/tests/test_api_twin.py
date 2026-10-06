"""API tests: Twin view, profile, skills, gaps, goals, projects."""

RESUME_TEXT = (
    "Priya Sharma. Python developer with Git, GitHub and SQL experience. "
    "Built machine learning models with scikit-learn. B.Tech Computer Science."
)


def test_empty_twin_shape(alice, client):
    response = client.get("/twin", headers=alice["headers"])
    assert response.status_code == 200
    twin = response.json()
    assert twin["skills"] == []
    assert twin["summary"]["skills_count"] == 0
    assert twin["summary"]["readiness_score"] == 0


def test_update_target_role_and_goal(alice, client):
    response = client.patch("/twin", headers=alice["headers"], json={
        "target_role": "AI Intern", "primary_goal": "Get an AI internship",
    })
    assert response.status_code == 200
    twin = response.json()
    assert twin["profile"]["target_role"] == "AI Intern"
    assert twin["role_key"] == "ai_intern"
    assert twin["summary"]["primary_goal"] == "Get an AI internship"


def test_manual_skill_add_and_history(alice, client):
    added = client.post("/twin/skills", headers=alice["headers"],
                        json={"name": "Python", "level": 3, "note": "self assessed"})
    assert added.status_code == 201
    assert added.json()["new_level"] == 3
    skills = client.get("/twin/skills", headers=alice["headers"]).json()["skills"]
    assert skills[0]["skill_name"] == "Python"
    history = client.get("/twin/skills/history", headers=alice["headers"]).json()["history"]
    assert history[0]["new_level"] == 3
    assert history[0]["source"] == "manual"


def test_gaps_computed_and_persisted(alice, client):
    client.patch("/twin", headers=alice["headers"], json={"target_role": "AI Intern"})
    gaps = client.get("/twin/gaps", headers=alice["headers"]).json()
    assert gaps["role_key"] == "ai_intern"
    assert len(gaps["gaps"]) > 0
    top = gaps["gaps"][0]
    assert {"skill_name", "current_level", "target_level", "gap", "priority",
            "reason", "recommended_action"} <= set(top)


def test_goals_crud(alice, client):
    created = client.post("/twin/goals", headers=alice["headers"],
                          json={"title": "AI Internship", "target_role": "AI Intern"})
    assert created.status_code == 201
    goal_id = created.json()["id"]
    updated = client.patch(f"/twin/goals/{goal_id}", headers=alice["headers"],
                           json={"status": "completed"})
    assert updated.json()["status"] == "completed"
    assert client.patch("/twin/goals/9999", headers=alice["headers"],
                        json={"status": "completed"}).status_code == 404


def test_completed_project_adds_skill_evidence(alice, client):
    response = client.post("/twin/projects", headers=alice["headers"], json={
        "title": "Churn model", "skills": ["Python", "Machine Learning"], "status": "completed",
    })
    assert response.status_code == 201
    skills = {s["skill_name"] for s in
              client.get("/twin/skills", headers=alice["headers"]).json()["skills"]}
    assert {"Python", "Machine Learning"} <= skills

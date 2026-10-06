"""API tests: resume analysis updates the Twin (nothing discarded)."""

import os

from tests.conftest import minimal_pdf_bytes

RESUME_TEXT = (
    "Aarav Patel\nPython developer. Built ML models with scikit-learn and SQL.\n"
    "Projects: Fraud Detection (Python, Machine Learning), Portfolio API (FastAPI).\n"
    "Git, GitHub. B.Tech 2024. github.com/aarav"
)


def test_analyze_text_updates_twin(alice, client):
    client.patch("/twin", headers=alice["headers"],
                 json={"target_role": "AI Intern", "primary_goal": "AI internship"})
    response = client.post("/resume/analyze", headers=alice["headers"],
                           json={"resume_text": RESUME_TEXT})
    assert response.status_code == 201
    body = response.json()
    assert "Python" in body["analysis"]["extracted_skills"]
    assert "Machine Learning" in body["analysis"]["extracted_skills"]
    assert body["analysis"]["readiness_score"] > 0
    assert len(body["twin_diff"]["skills_added"]) >= 3
    assert body["twin_diff"]["projects_imported"] >= 1

    twin = client.get("/twin", headers=alice["headers"]).json()
    names = {s["skill_name"] for s in twin["skills"]}
    assert {"Python", "Machine Learning"} <= names
    assert twin["summary"]["skills_count"] >= 3
    assert len(twin["projects"]) >= 1

    history = client.get("/resume/history", headers=alice["headers"]).json()
    assert len(history["analyses"]) == 1


def test_upload_pdf_end_to_end(alice, client, tmp_env):
    pdf = minimal_pdf_bytes([
        "Jane Doe", "Python Git SQL Machine Learning",
        "Projects: Chatbot with NLP and FastAPI",
    ])
    response = client.post(
        "/resume/upload", headers=alice["headers"],
        files={"file": ("resume.pdf", pdf, "application/pdf")},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert "Python" in body["analysis"]["extracted_skills"]
    assert body["resume"]["filename_stored"].endswith(".pdf")
    assert body["resume"]["filename_stored"] != "resume.pdf"  # UUID-renamed
    stored = os.path.join(tmp_env["uploads"], body["resume"]["filename_stored"])
    assert os.path.exists(stored)

    twin = client.get("/twin", headers=alice["headers"]).json()
    assert twin["summary"]["skills_count"] >= 2


def test_short_text_rejected(alice, client):
    response = client.post("/resume/analyze", headers=alice["headers"],
                           json={"resume_text": "too short"})
    assert response.status_code == 422

"""Personalized roadmap engine.

Roadmaps are generated from the user's actual gaps: each open gap becomes
one focused learning item, ordered by priority, followed by a project item
and an application item that reference the user's real state. Completing
an item feeds skill evidence back into the Twin.
"""

from app.db import content as content_repo
from app.db import memory as memory_repo
from app.twin import service as twin_service

DIFFICULTY_BY_LEVEL = {0: "beginner", 1: "beginner", 2: "beginner", 3: "intermediate",
                       4: "intermediate", 5: "advanced"}
EFFORT_BY_GAP = {1: "3-5 hours", 2: "1 week", 3: "2 weeks", 4: "3-4 weeks", 5: "4+ weeks"}

SKILL_RESOURCES = {
    "Python": ["https://docs.python.org/3/tutorial/", "https://realpython.com/"],
    "Git": ["https://git-scm.com/book/en/v2", "https://learngitbranching.js.org/"],
    "GitHub": ["https://docs.github.com/", "https://skills.github.com/"],
    "SQL": ["https://www.postgresql.org/docs/current/tutorial.html",
            "https://sqlbolt.com/"],
    "FastAPI": ["https://fastapi.tiangolo.com/tutorial/",
                "https://fastapi.tiangolo.com/tutorial/testing/"],
    "Docker": ["https://docs.docker.com/get-started/", "https://docs.docker.com/compose/"],
    "Machine Learning": ["https://scikit-learn.org/stable/tutorial/",
                         "https://developers.google.com/machine-learning/crash-course"],
    "Deep Learning": ["https://pytorch.org/tutorials/",
                      "https://course.fast.ai/"],
    "Data Analysis": ["https://pandas.pydata.org/docs/getting_started/",
                      "https://www.kaggle.com/learn"],
    "default": ["https://developer.mozilla.org/", "https://www.khanacademy.org/"],
}


class RoadmapService:
    def generate(self, user_id: str, goal: str | None = None) -> dict:
        gaps, _ = twin_service.get_gaps(user_id, persist=True)
        summary = twin_service.build_summary(user_id)
        goal_text = goal or summary.primary_goal or summary.target_role or "Career growth"
        roadmap = content_repo.create_roadmap(user_id, goal_text)

        items: list = []
        position = 0
        previous_title: str | None = None
        for gap in gaps[:8]:
            title = f"Level up {gap.skill_name} ({gap.current_level}/5 → {gap.target_level}/5)"
            item = content_repo.create_roadmap_item(roadmap["id"], user_id, {
                "title": title,
                "description": (
                    f"{gap.reason} Focus block: study {gap.skill_name} fundamentals, "
                    f"then build one small exercise proving level {gap.target_level}."
                ),
                "skill": gap.skill_name,
                "difficulty": DIFFICULTY_BY_LEVEL.get(gap.current_level, "beginner"),
                "estimated_effort": EFFORT_BY_GAP.get(max(1, gap.gap), "1 week"),
                "priority": gap.priority,
                "dependencies": [previous_title] if previous_title else [],
                "resources": SKILL_RESOURCES.get(gap.skill_name, SKILL_RESOURCES["default"]),
                "position": position,
            })
            items.append(item)
            previous_title = title
            position += 1

        project_skill = gaps[0].skill_name if gaps else (summary.top_gaps[0] if summary.top_gaps else "Python")
        items.append(content_repo.create_roadmap_item(roadmap["id"], user_id, {
            "title": f"Build a portfolio project using {project_skill}",
            "description": (
                f"Apply {project_skill} plus your strongest skills in one deployable "
                f"project with a README, tests and a live demo."
            ),
            "skill": project_skill,
            "difficulty": "intermediate",
            "estimated_effort": "2-3 weeks",
            "priority": "high",
            "dependencies": [previous_title] if previous_title else [],
            "resources": ["https://github.com/", "https://roadmap.sh/"],
            "position": position,
        }))
        position += 1
        items.append(content_repo.create_roadmap_item(roadmap["id"], user_id, {
            "title": f"Apply for {summary.target_role or 'target'} roles",
            "description": (
                "Tailor your resume to each application, highlight the project above, "
                "and track every application and outcome."
            ),
            "skill": "",
            "difficulty": "beginner",
            "estimated_effort": "ongoing",
            "priority": "medium",
            "dependencies": [],
            "resources": ["https://www.linkedin.com/jobs/", "https://internshala.com/"],
            "position": position,
        }))

        memory_repo.record_event(user_id, "roadmap_generated", ref_type="roadmap",
                                 ref_id=str(roadmap["id"]),
                                 data={"goal": goal_text, "items": len(items)})
        return {"roadmap": roadmap, "items": items}

    def get_active(self, user_id: str) -> dict | None:
        roadmap = content_repo.get_active_roadmap(user_id)
        if not roadmap:
            return None
        items = content_repo.list_roadmap_items(roadmap["id"], user_id)
        total = len(items)
        done = sum(1 for item in items if item["status"] == "completed")
        return {
            "roadmap": roadmap,
            "items": items,
            "progress": {
                "total": total,
                "completed": done,
                "percent": round(done / total * 100) if total else 0,
            },
        }

    def complete_item(self, user_id: str, item_id: int) -> dict:
        item = content_repo.get_roadmap_item(user_id, item_id)
        if not item:
            raise LookupError("Roadmap item not found.")
        if item["status"] == "completed":
            return {"item": item, "twin_change": None, "already_completed": True}
        updated = content_repo.update_roadmap_item(user_id, item_id, {"status": "completed"})
        memory_repo.record_event(
            user_id, "roadmap_item_completed", ref_type="roadmap_item",
            ref_id=str(item_id),
            data={"title": item["title"], "skill": item.get("skill", "")},
        )
        twin_change = None
        if item.get("skill"):
            twin_change = twin_service.add_skill_evidence(
                user_id, item["skill"], source="roadmap",
                note=f"Completed roadmap item: {item['title']}",
            )
        gaps, _ = twin_service.get_gaps(user_id, persist=True)
        return {"item": updated, "twin_change": twin_change,
                "already_completed": False, "open_gaps": len(gaps)}

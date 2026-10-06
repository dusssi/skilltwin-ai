"""Roadmap agent: ensures a fresh personalized roadmap exists."""

from app.db import content as content_repo
from app.roadmap.service import RoadmapService


class RoadmapAgent:
    name = "roadmap_agent"

    def __init__(self):
        self.service = RoadmapService()

    def run(self, user_id: str, goal: str = "", force: bool = False) -> dict:
        active = self.service.get_active(user_id)
        if active and not force:
            return {"roadmap": active["roadmap"], "items": active["items"],
                    "progress": active["progress"], "regenerated": False}
        generated = self.service.generate(user_id, goal=goal or None)
        items = generated["items"]
        done = sum(1 for item in items if item["status"] == "completed")
        return {"roadmap": generated["roadmap"], "items": items,
                "progress": {"total": len(items), "completed": done,
                             "percent": round(done / len(items) * 100) if items else 0},
                "regenerated": True}

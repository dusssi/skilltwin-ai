"""Gap-driven recommendation engine (projects, internships, next actions).

Recommendations are computed from the user's real Twin: project fit is the
overlap between catalog skills and the user's gaps + strengths; internship
fit requires the user to already show the core skills.
"""

from app.db import content as content_repo
from app.db import twin as twin_repo
from app.recommendations.catalog import INTERNSHIP_CATALOG, PROJECT_CATALOG
from app.twin import service as twin_service


class RecommendationEngine:
    def generate(self, user_id: str) -> dict:
        skills = {s["skill_name"]: s for s in
                  __import__("app.db.twin", fromlist=["list_user_skills"]).list_user_skills(user_id)}
        gaps, _ = twin_service.get_gaps(user_id, persist=False)
        gap_names = [gap.skill_name for gap in gaps]

        content_repo.clear_suggested_recommendations(user_id)

        projects = self._rank_projects(skills, gap_names)
        internships = self._rank_internships(skills)
        actions = self._next_actions(gaps)

        stored = {"projects": [], "internships": [], "actions": []}
        for project in projects[:3]:
            stored["projects"].append(content_repo.create_recommendation(
                user_id, "project", project["title"], project))
        for internship in internships[:3]:
            stored["internships"].append(content_repo.create_recommendation(
                user_id, "internship", internship["title"], internship))
        for action in actions[:3]:
            stored["actions"].append(content_repo.create_recommendation(
                user_id, "action", action["title"], action))
        return stored

    def _rank_projects(self, skills: dict, gap_names: list) -> list:
        ranked = []
        for project in PROJECT_CATALOG:
            required = project["skills"]
            have = sum(1 for skill in required if skill in skills)
            closes_gap = sum(1 for skill in required if skill in gap_names)
            score = have * 2 + closes_gap * 3 - max(0, len(required) - have)
            ranked.append({**project, "match_score": score,
                           "matched_skills": [s for s in required if s in skills],
                           "gap_skills": [s for s in required if s in gap_names]})
        ranked.sort(key=lambda item: item["match_score"], reverse=True)
        return ranked

    def _rank_internships(self, skills: dict) -> list:
        ranked = []
        for internship in INTERNSHIP_CATALOG:
            required = internship["skills"]
            have = [skill for skill in required if skill in skills]
            missing = [skill for skill in required if skill not in skills]
            ranked.append({**internship, "matched_skills": have,
                           "missing_skills": missing,
                           "ready": not missing,
                           "match_score": len(have) - len(missing)})
        ranked.sort(key=lambda item: (item["ready"], item["match_score"]), reverse=True)
        return ranked

    def _next_actions(self, gaps: list) -> list:
        actions = []
        for gap in gaps[:3]:
            actions.append({
                "title": f"Close gap: {gap.skill_name}",
                "detail": gap.reason,
                "recommended_action": gap.recommended_action,
                "priority": gap.priority,
            })
        return actions

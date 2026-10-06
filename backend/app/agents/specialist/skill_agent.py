"""Skill analysis agent: computes real gaps from the Twin."""

from app.twin import service as twin_service


class SkillAgent:
    name = "skill_agent"

    def run(self, user_id: str) -> dict:
        gaps, role_key = twin_service.get_gaps(user_id, persist=True)
        return {
            "role_key": role_key,
            "gaps": [gap.model_dump() for gap in gaps],
            "open_count": len(gaps),
        }

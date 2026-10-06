"""Structured skill-gap engine.

Gaps are computed from the difference between the user's current Skill Twin
levels and the target-role rubric. Priority combines gap size, importance
for the role, and current proficiency:

    score = gap * importance + (2 if current_level <= 1 else 0)

score >= 12      -> critical
score >= 8       -> high
score >= 4       -> medium
otherwise        -> low
"""

from app.twin.models import SkillGap
from app.twin.role_profiles import get_role_profile, match_role


def _priority_for(score: int) -> str:
    if score >= 12:
        return "critical"
    if score >= 8:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


def compute_gaps(
    user_skills: list,
    target_role: str,
    role_key: str | None = None,
) -> list[SkillGap]:
    key = role_key or match_role(target_role)
    profile = get_role_profile(key)
    current_by_name = {skill["skill_name"]: skill for skill in user_skills}

    gaps: list[SkillGap] = []
    for skill_name, rubric in profile["skills"].items():
        target = int(rubric["target"])
        importance = int(rubric["importance"])
        current = current_by_name.get(skill_name)
        current_level = int(current["level"]) if current else 0
        gap_size = max(0, target - current_level)
        if gap_size == 0:
            continue
        score = gap_size * importance + (2 if current_level <= 1 else 0)
        priority = _priority_for(score)
        if current_level == 0:
            reason = (
                f"Required for {profile['label']} (target {target}/5); "
                "no evidence of this skill in your Twin yet."
            )
        else:
            reason = (
                f"Required for {profile['label']} at {target}/5; "
                f"currently {current_level}/5."
            )
        gaps.append(
            SkillGap(
                skill_name=skill_name,
                current_level=current_level,
                target_level=target,
                gap=gap_size,
                priority=priority,
                importance=importance,
                reason=reason,
                recommended_action=f"Complete a guided learning block for {skill_name}.",
            )
        )

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    gaps.sort(key=lambda gap: (order[gap.priority], -gap.gap, gap.skill_name))
    return gaps

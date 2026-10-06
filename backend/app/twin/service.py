"""Skill Twin service: the evolving career representation of a user.

The Twin is *merged*, never blindly overwritten:

* new evidence is appended to a skill's evidence list,
* level only moves up (or stays) when credible evidence arrives,
* every level change is recorded in ``skill_history`` with reason + source,
* every meaningful change emits a progress event.

Levels are 1-5. ``target_level`` comes from the active role rubric.
"""

from app.db import content as content_repo
from app.db import memory as memory_repo
from app.db import twin as twin_repo
from app.db.database import utcnow
from app.twin.gaps import compute_gaps
from app.twin.models import TwinSummary
from app.twin.role_profiles import get_role_profile, match_role

#: Sources trusted to raise a skill level, with the minimum level they imply.
SOURCE_LEVEL_HINTS = {
    "resume": 2,
    "chat": 1,
    "roadmap": 3,
    "project": 3,
    "manual": 2,
    "assessment": 3,
    "agent": 2,
}


def _confidence_for(evidence: list) -> float:
    sources = {item.get("source", "") for item in evidence if isinstance(item, dict)}
    base = 0.35 + 0.1 * min(len(evidence), 4)
    bonus = 0.1 * max(0, len(sources) - 1)
    return round(min(0.95, base + bonus), 2)


def add_skill_evidence(
    user_id: str,
    skill_name: str,
    source: str,
    note: str = "",
    level_hint: int | None = None,
    category: str = "",
) -> dict:
    """Merge one piece of evidence into the Twin. Returns change summary."""
    name = (skill_name or "").strip()
    if not name:
        raise ValueError("skill_name is required")
    skill = twin_repo.ensure_skill(name, category=category)
    existing = twin_repo.get_user_skill(user_id, skill["id"])

    old_level = int(existing["level"]) if existing else 0
    evidence = list(existing["evidence"]) if existing else []
    evidence.append({"source": source, "note": note or "", "at": utcnow()})

    hint = level_hint if level_hint else SOURCE_LEVEL_HINTS.get(source, 1)
    hint = max(1, min(5, int(hint)))

    profile = twin_repo.get_profile(user_id) or {}
    role_key = match_role(profile.get("target_role", ""))
    rubric = get_role_profile(role_key)["skills"].get(name, {})
    target_level = int(rubric.get("target", 4))
    if existing:
        target_level = max(int(existing["target_level"]), target_level)

    # Roadmap/project evidence can push a level up when sustained.
    sustained_sources = {item.get("source") for item in evidence if isinstance(item, dict)}
    new_level = max(old_level, hint)
    if source in {"roadmap", "project"} and len(evidence) >= 2:
        new_level = max(new_level, min(5, old_level + 1) if old_level else hint)
    if len(sustained_sources) >= 3 and new_level < 5 and old_level:
        new_level = min(5, old_level + 1)

    record = twin_repo.upsert_user_skill(
        user_id=user_id,
        skill_id=skill["id"],
        level=new_level,
        target_level=target_level,
        confidence=_confidence_for(evidence),
        evidence=evidence,
    )

    leveled_up = new_level > old_level
    if leveled_up:
        twin_repo.add_skill_history(
            user_id=user_id,
            skill_id=skill["id"],
            old_level=old_level,
            new_level=new_level,
            reason=note or f"Evidence from {source}",
            source=source,
        )
        memory_repo.record_event(
            user_id,
            "skill_improved" if old_level else "skill_detected",
            ref_type="skill",
            ref_id=str(skill["id"]),
            data={"skill": name, "old_level": old_level, "new_level": new_level,
                  "source": source},
        )
    return {
        "skill": name,
        "old_level": old_level,
        "new_level": new_level,
        "leveled_up": leveled_up,
        "evidence_count": len(evidence),
        "record": record,
    }


def set_target_role(user_id: str, target_role: str) -> dict:
    """Change target role and refresh every skill's target level from the rubric."""
    profile = twin_repo.update_profile(user_id, {"target_role": target_role})
    role_key = match_role(target_role)
    rubric = get_role_profile(role_key)["skills"]
    for skill in twin_repo.list_user_skills(user_id):
        name = skill["skill_name"]
        if name in rubric:
            twin_repo.upsert_user_skill(
                user_id=user_id,
                skill_id=skill["skill_id"],
                level=skill["level"],
                target_level=int(rubric[name]["target"]),
                confidence=skill["confidence"],
                evidence=skill["evidence"],
            )
    memory_repo.record_event(
        user_id, "target_role_changed", data={"target_role": target_role, "role_key": role_key}
    )
    return profile


def get_gaps(user_id: str, persist: bool = True) -> tuple[list, str]:
    profile = twin_repo.get_profile(user_id) or {}
    target_role = profile.get("target_role", "")
    role_key = match_role(target_role)
    skills = twin_repo.list_user_skills(user_id)
    gaps = compute_gaps(skills, target_role, role_key=role_key)
    if persist:
        twin_repo.save_gap_snapshot(user_id, [gap.model_dump() for gap in gaps])
    return gaps, role_key


def build_summary(user_id: str) -> TwinSummary:
    profile = twin_repo.get_profile(user_id) or {}
    skills = twin_repo.list_user_skills(user_id)
    gaps, role_key = get_gaps(user_id, persist=False)
    projects = twin_repo.list_projects(user_id)
    events = memory_repo.list_events(user_id, limit=8)

    roadmap_progress: dict = {}
    roadmap = content_repo.get_active_roadmap(user_id)
    if roadmap:
        items = content_repo.list_roadmap_items(roadmap["id"], user_id)
        total = len(items)
        done = sum(1 for item in items if item["status"] == "completed")
        roadmap_progress = {
            "roadmap_id": roadmap["id"],
            "goal": roadmap["goal"],
            "total": total,
            "completed": done,
            "percent": round(done / total * 100) if total else 0,
        }

    avg_level = round(sum(s["level"] for s in skills) / len(skills), 2) if skills else 0.0
    readiness = _readiness_score(skills, gaps, projects, roadmap_progress)
    return TwinSummary(
        display_name=profile.get("display_name", ""),
        target_role=profile.get("target_role", ""),
        role_key=role_key,
        primary_goal=profile.get("primary_goal", ""),
        experience_years=float(profile.get("experience_years", 0) or 0),
        education=profile.get("education", ""),
        skills_count=len(skills),
        avg_level=avg_level,
        gaps_count=len(gaps),
        top_gaps=[gap.skill_name for gap in gaps[:5]],
        projects_count=len(projects),
        roadmap_progress=roadmap_progress,
        readiness_score=readiness,
        recent_events=[
            {"type": event["event_type"], "data": event["data"],
             "at": event["created_at"]}
            for event in events
        ],
    )


def _readiness_score(skills: list, gaps: list, projects: list, roadmap_progress: dict) -> int:
    """Deterministic 0-100 readiness score from real Twin state."""
    if not skills and not projects:
        return 0
    rubric_total = max(1, len(gaps) + sum(1 for _ in skills))
    closed_share = 1 - len(gaps) / max(1, len(gaps) + len(skills))
    level_share = (
        sum(min(s["level"], 5) for s in skills) / (len(skills) * 5) if skills else 0
    )
    project_share = min(1.0, len(projects) / 3)
    roadmap_share = (roadmap_progress.get("percent", 0) / 100) if roadmap_progress else 0
    score = (
        0.35 * closed_share + 0.3 * level_share + 0.2 * project_share + 0.15 * roadmap_share
    )
    return int(round(score * 100))


def full_twin(user_id: str) -> dict:
    """Complete Twin view: profile, skills+history, gaps, goals, projects."""
    profile = twin_repo.get_profile(user_id) or {}
    skills = twin_repo.list_user_skills(user_id)
    history = twin_repo.list_skill_history(user_id, limit=200)
    history_by_skill: dict = {}
    for entry in history:
        history_by_skill.setdefault(entry["skill_name"], []).append(entry)
    for skill in skills:
        skill["history"] = history_by_skill.get(skill["skill_name"], [])
    gaps, role_key = get_gaps(user_id, persist=False)
    return {
        "profile": profile,
        "role_key": role_key,
        "skills": skills,
        "gaps": [gap.model_dump() for gap in gaps],
        "goals": twin_repo.list_goals(user_id),
        "projects": twin_repo.list_projects(user_id),
        "summary": build_summary(user_id).model_dump(),
    }

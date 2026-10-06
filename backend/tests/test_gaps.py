"""Unit tests for the skill-gap engine."""

from app.twin.gaps import compute_gaps


def _skill(name, level):
    return {"skill_name": name, "level": level}


def test_unknown_skills_produce_gaps():
    gaps = compute_gaps([], "AI Intern")
    assert len(gaps) > 0
    names = {gap.skill_name for gap in gaps}
    assert "Python" in names and "Git" in names
    for gap in gaps:
        assert gap.current_level == 0
        assert gap.gap == gap.target_level


def test_met_skills_are_not_gaps():
    skills = [_skill("Python", 5), _skill("Git", 5), _skill("GitHub", 5),
              _skill("Machine Learning", 5), _skill("SQL", 5), _skill("FastAPI", 5),
              _skill("Docker", 5), _skill("Data Analysis", 5), _skill("Mathematics", 5),
              _skill("Communication", 5)]
    gaps = compute_gaps([], "something unrelated")
    assert gaps  # general rubric still applies
    ai_gaps = compute_gaps(skills, "AI Intern")
    assert ai_gaps == []


def test_priority_ordering_critical_first():
    gaps = compute_gaps([_skill("Python", 4)], "AI Intern")
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    ranks = [order[gap.priority] for gap in gaps]
    assert ranks == sorted(ranks)


def test_gap_fields_complete():
    gaps = compute_gaps([], "Backend Developer")
    gap = next(g for g in gaps if g.skill_name == "FastAPI")
    assert gap.target_level == 4
    assert gap.priority in {"critical", "high", "medium", "low"}
    assert gap.reason
    assert gap.recommended_action


def test_role_matching():
    assert compute_gaps([], "I want a data analyst job")
    gaps = compute_gaps([], "frontend developer")
    assert any(g.skill_name == "React" for g in gaps)

"""Unit tests for typed reflection and planning."""

from app.planner.planner import Planner
from app.reflection.models import ReflectionInput
from app.reflection.reflector import Reflector


def test_reflection_scores_progress():
    result = Reflector().reflect(ReflectionInput(
        goal="AI Internship", gaps_closed=6, gaps_open=2,
        roadmap_completed=4, roadmap_total=5,
        skills_improved=["Python", "Git"], recent_events=["resume_uploaded"],
    ))
    assert 6 <= result.score <= 10
    assert result.issues
    assert result.suggestions
    assert result.narrative


def test_reflection_flags_stalled_state():
    result = Reflector().reflect(ReflectionInput(
        goal="AI Internship", gaps_closed=0, gaps_open=8,
        roadmap_completed=0, roadmap_total=0,
        skills_improved=[], recent_events=[],
    ))
    assert result.score <= 5
    assert any("gap" in issue for issue in result.issues)


def test_planner_adapts_to_state():
    plan = Planner().create_plan("AI Internship", {"gaps_open": 5, "roadmap_total": 0,
                                                   "skills_count": 3})
    names = [step.name for step in plan.steps]
    assert names[0] == "observe"
    assert "analyze_gaps" in names
    assert "generate_roadmap" in names
    assert names[-1] == "reflect"


def test_planner_skips_roadmap_when_present():
    plan = Planner().create_plan("AI Internship", {"gaps_open": 2, "roadmap_total": 6,
                                                   "skills_count": 5})
    names = [step.name for step in plan.steps]
    assert "generate_roadmap" not in names
    assert "recommend" in names


def test_planner_bootstraps_empty_twin():
    plan = Planner().create_plan("AI Internship", {"gaps_open": 0, "roadmap_total": 0,
                                                   "skills_count": 0})
    assert "bootstrap_twin" in [step.name for step in plan.steps]

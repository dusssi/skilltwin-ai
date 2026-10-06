"""Pydantic models describing the Skill Twin."""

from pydantic import BaseModel, Field


class SkillEvidence(BaseModel):
    source: str = ""
    note: str = ""
    at: str = ""


class TwinSkill(BaseModel):
    name: str
    level: int = 1
    target_level: int = 4
    confidence: float = 0.5
    evidence: list[SkillEvidence] = Field(default_factory=list)
    history: list[dict] = Field(default_factory=list)
    updated_at: str = ""


class SkillGap(BaseModel):
    skill_name: str
    current_level: int
    target_level: int
    gap: int
    priority: str
    importance: int = 3
    reason: str = ""
    recommended_action: str = ""


class TwinSummary(BaseModel):
    display_name: str = ""
    target_role: str = ""
    role_key: str = "general"
    primary_goal: str = ""
    experience_years: float = 0.0
    education: str = ""
    skills_count: int = 0
    avg_level: float = 0.0
    gaps_count: int = 0
    top_gaps: list[str] = Field(default_factory=list)
    projects_count: int = 0
    roadmap_progress: dict = Field(default_factory=dict)
    readiness_score: int = 0
    recent_events: list[dict] = Field(default_factory=list)

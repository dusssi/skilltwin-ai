"""Reflection models (typed agent I/O)."""

from pydantic import BaseModel, Field


class ReflectionInput(BaseModel):
    goal: str = ""
    gaps_closed: int = 0
    gaps_open: int = 0
    roadmap_completed: int = 0
    roadmap_total: int = 0
    skills_improved: list[str] = Field(default_factory=list)
    recent_events: list[str] = Field(default_factory=list)


class ReflectionResult(BaseModel):
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    score: int = 0
    narrative: str = ""

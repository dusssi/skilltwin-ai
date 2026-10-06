"""Typed agent-run state (the single orchestration data contract)."""

from pydantic import BaseModel, Field

from app.planner.planner import Plan


class Observation(BaseModel):
    text: str


class AgentRunState(BaseModel):
    user_id: str
    goal: str = ""
    observations: list[str] = Field(default_factory=list)
    plan: Plan = Field(default_factory=Plan)
    gaps: list[dict] = Field(default_factory=list)
    roadmap: dict = Field(default_factory=dict)
    recommendations: dict = Field(default_factory=dict)
    research: dict = Field(default_factory=dict)
    reflection: dict = Field(default_factory=dict)
    completed_steps: list[str] = Field(default_factory=list)
    status: str = "initialized"
    summary: str = ""

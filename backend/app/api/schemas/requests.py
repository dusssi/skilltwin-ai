"""API request schemas."""

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(default="", max_length=80)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=1, max_length=128)


class TwinUpdateRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=80)
    target_role: str | None = Field(default=None, max_length=120)
    primary_goal: str | None = Field(default=None, max_length=300)
    experience_years: float | None = Field(default=None, ge=0, le=60)
    education: str | None = Field(default=None, max_length=500)
    preferences: dict | None = None


class SkillAddRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    level: int | None = Field(default=None, ge=1, le=5)
    note: str = Field(default="", max_length=500)


class GoalCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    target_role: str = Field(default="", max_length=120)


class GoalUpdateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    target_role: str | None = Field(default=None, max_length=120)
    status: str | None = Field(default=None, pattern=r"^(active|completed|archived)$")


class ProjectCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    skills: list[str] = Field(default_factory=list, max_length=30)
    status: str = Field(default="planned", pattern=r"^(planned|in_progress|completed)$")


class ResumeTextRequest(BaseModel):
    resume_text: str = Field(min_length=20, max_length=60000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=64)


class RoadmapGenerateRequest(BaseModel):
    goal: str | None = Field(default=None, max_length=300)


class RoadmapItemUpdateRequest(BaseModel):
    status: str = Field(pattern=r"^(pending|in_progress|completed|skipped)$")


class RuntimeRequest(BaseModel):
    goal: str | None = Field(default=None, max_length=300)


class MemoryCreateRequest(BaseModel):
    kind: str = Field(default="fact", max_length=32)
    content: str = Field(min_length=1, max_length=2000)
    importance: int = Field(default=5, ge=1, le=10)


class RecommendationStatusRequest(BaseModel):
    status: str = Field(pattern=r"^(suggested|accepted|dismissed|completed)$")

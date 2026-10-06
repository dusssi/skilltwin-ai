"""Resume analysis models."""

from pydantic import BaseModel, Field


class ResumeExperience(BaseModel):
    years: float = 0.0
    roles: list[str] = Field(default_factory=list)
    seniority: str = "unknown"


class ResumeProject(BaseModel):
    title: str
    detail: str = ""
    skills: list[str] = Field(default_factory=list)


class ResumeAnalysis(BaseModel):
    extracted_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    experience: ResumeExperience = Field(default_factory=ResumeExperience)
    projects: list[ResumeProject] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    career_signals: list[str] = Field(default_factory=list)
    readiness_score: int = 0

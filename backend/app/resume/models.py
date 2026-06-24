from pydantic import (
    BaseModel,
    Field
)

from typing import List


class ResumeAnalysis(
    BaseModel
):

    extracted_skills: List[str] = Field(
        default_factory=list
    )

    missing_skills: List[str] = Field(
        default_factory=list
    )

    recommended_projects: List[str] = Field(
        default_factory=list
    )

    readiness_score: int = 0
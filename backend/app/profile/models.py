from pydantic import (
    BaseModel,
    Field
)

from typing import List


class UserProfile(
    BaseModel
):

    user_id: str

    primary_goal: str = ""

    skills: List[str] = Field(
        default_factory=list
    )

    missing_skills: List[str] = Field(
        default_factory=list
    )

    projects: List[str] = Field(
        default_factory=list
    )

    reflection_score: int = 0
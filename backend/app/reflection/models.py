from pydantic import BaseModel, Field

from typing import List


class ReflectionResult(BaseModel):

    issues: List[str] = Field(
        default_factory=list
    )

    suggestions: List[str] = Field(
        default_factory=list
    )

    score: int = 0
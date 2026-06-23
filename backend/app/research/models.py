from pydantic import BaseModel, Field

from typing import List


class ResearchResult(BaseModel):

    query: str

    evidence: List[str] = Field(
        default_factory=list
    )

    conclusion: str = ""
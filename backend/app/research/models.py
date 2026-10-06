"""Research models (typed agent I/O)."""

from pydantic import BaseModel, Field


class ResearchResult(BaseModel):
    query: str
    evidence: list[str] = Field(default_factory=list)
    conclusion: str = ""
    sources: list[str] = Field(default_factory=list)

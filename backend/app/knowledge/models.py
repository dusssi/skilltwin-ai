"""Knowledge base models."""

from pydantic import BaseModel, Field


class KnowledgeItem(BaseModel):
    topic: str
    facts: list[str] = Field(default_factory=list)


class RetrievalResult(BaseModel):
    topic: str
    score: float
    facts: list[str] = Field(default_factory=list)

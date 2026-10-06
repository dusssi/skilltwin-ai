"""LLM response models."""

from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    content: str
    provider: str
    model: str
    fallback: bool = False


class ChatTwinUpdate(BaseModel):
    """Structured facts extracted from a user message to evolve the Twin."""

    mentioned_skills: list[str] = Field(default_factory=list)
    goal_statement: str = ""
    completed_activity: str = ""
    preference_statement: str = ""

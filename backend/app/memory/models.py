"""Memory models (DB-backed)."""

from pydantic import BaseModel, Field


class Memory(BaseModel):
    id: int = 0
    user_id: str = ""
    kind: str = ""
    content: str = ""
    importance: int = 5
    created_at: str = ""
    updated_at: str = ""


class ProgressEvent(BaseModel):
    id: int = 0
    user_id: str = ""
    event_type: str = ""
    ref_type: str = ""
    ref_id: str = ""
    data: dict = Field(default_factory=dict)
    created_at: str = ""


class MemoryRecord(BaseModel):
    """Legacy-compatible summary of a user's durable memory."""

    user_id: str
    goal: str = ""
    completed_tasks: list[str] = Field(default_factory=list)
    observations: list[str] = Field(default_factory=list)

"""Session models (DB-backed)."""

from pydantic import BaseModel, Field


class Session(BaseModel):
    session_id: str = ""
    user_id: str = ""
    messages: list[str] = Field(default_factory=list)
    summary: str = ""
    created_at: str = ""


class StoredSession(BaseModel):
    id: str
    user_id: str
    summary: str = ""
    created_at: str = ""
    updated_at: str = ""


class Message(BaseModel):
    id: int = 0
    session_id: str = ""
    user_id: str = ""
    role: str = ""
    content: str = ""
    created_at: str = ""

from pydantic import BaseModel, Field

from typing import List

from datetime import datetime


class Session(BaseModel):

    session_id: str

    user_id: str

    messages: List[str] = Field(
        default_factory=list
    )

    summary: str = ""

    created_at: str = Field(
        default_factory=lambda:
        datetime.now().isoformat()
    )
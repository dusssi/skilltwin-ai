from pydantic import BaseModel, Field

from typing import List


class KnowledgeItem(BaseModel):

    topic: str

    facts: List[str] = Field(
        default_factory=list
    )
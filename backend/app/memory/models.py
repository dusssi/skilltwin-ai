from pydantic import BaseModel
from typing import List


class MemoryRecord(BaseModel):

    user_id: str

    goal: str

    completed_tasks: List[str] = []

    observations: List[str] = []
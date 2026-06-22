from pydantic import BaseModel, Field
from typing import List


class AgentState(BaseModel):
    """
    Runtime state for SkillTwin AI

    Inspired By:
    - Claw Code Runtime
    - Claude Code State Architecture
    """

    # User's primary goal
    user_goal: str

    # Planner generated tasks
    current_plan: List[str] = Field(
        default_factory=list
    )

    # Finished tasks
    completed_tasks: List[str] = Field(
        default_factory=list
    )

    # Agent discoveries
    observations: List[str] = Field(
        default_factory=list
    )

    # Final answer returned to user
    final_response: str = ""

    # Runtime loop count
    iteration_count: int = 0
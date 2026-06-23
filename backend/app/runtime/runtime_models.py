from pydantic import (
    BaseModel,
    Field
)

from typing import List


class RuntimeState(
    BaseModel
):

    # User Goal

    goal: str

    # Runtime Plan

    plan: List[str] = Field(
        default_factory=list
    )

    # Current Task

    current_task: str = ""

    # Finished Tasks

    completed_tasks: List[str] = Field(
        default_factory=list
    )

    # Observations

    observations: List[str] = Field(
        default_factory=list
    )

    # Profile Snapshot

    profile_snapshot: dict = Field(
        default_factory=dict
    )

    # Real Action Results

    action_results: dict = Field(
        default_factory=dict
    )

    # Actions Executed

    actions_taken: List[str] = Field(
        default_factory=list
    )

    # Runtime Iterations

    iteration_count: int = 0

    # Runtime Status

    status: str = "initialized"
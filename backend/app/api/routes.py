from fastapi import APIRouter

from app.agents.orchestrator import (
    OrchestratorAgent
)

router = APIRouter()


@router.post("/goal")
def process_goal(
    data: dict
):

    goal = data["goal"]

    agent = OrchestratorAgent()

    result = agent.run(goal)

    return result
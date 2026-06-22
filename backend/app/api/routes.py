from fastapi import APIRouter

from app.agents.orchestrator import (
    OrchestratorAgent
)

router = APIRouter()


@router.post("/goal")
def process_goal(
    data: dict
):

    user_id = data["user_id"]

    session_id = data["session_id"]

    goal = data["goal"]

    agent = OrchestratorAgent()

    result = agent.run(
        user_id=user_id,
        session_id=session_id,
        goal=goal
    )

    return result
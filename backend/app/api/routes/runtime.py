"""Agent runtime route: runs the canonical orchestrator."""

from fastapi import APIRouter, Depends

from app.agents.orchestrator import OrchestratorAgent
from app.api.schemas.requests import RuntimeRequest
from app.auth.dependencies import get_current_user

router = APIRouter(tags=["runtime"])

orchestrator = OrchestratorAgent()


@router.post("/runtime")
def run_runtime(payload: RuntimeRequest, user: dict = Depends(get_current_user)):
    state = orchestrator.run(user["id"], goal=payload.goal)
    return {
        "status": state.status,
        "result": {
            "goal": state.goal,
            "observations": state.observations,
            "plan": state.plan.model_dump(),
            "completed_steps": state.completed_steps,
            "gaps": state.gaps,
            "roadmap": state.roadmap,
            "recommendations": state.recommendations,
            "research": state.research,
            "reflection": state.reflection,
            "summary": state.summary,
        },
    }

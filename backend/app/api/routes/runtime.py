from fastapi import APIRouter

from app.api.schemas.requests import (
    RuntimeRequest
)

from app.api.schemas.responses import (
    RuntimeResponse
)

from app.runtime.runtime_loop import (
    RuntimeLoop
)

router = APIRouter()

runtime = RuntimeLoop()


@router.post(
    "/runtime",
    response_model=RuntimeResponse
)
def run_runtime(
    request: RuntimeRequest
):

    state = runtime.run(

        goal=request.goal,

        user_id=request.user_id
    )

    return RuntimeResponse(

        status=state.status,

        result={

            "goal":
            state.goal,

            "iterations":
            state.iteration_count,

            "completed_tasks":
            state.completed_tasks,

            "reflection":
            state.reflection_results,

            "observations":
            state.observations
        }
    )
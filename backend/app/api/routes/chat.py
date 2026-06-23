from fastapi import APIRouter

from app.api.schemas.requests import (
    ChatRequest
)

from app.api.schemas.responses import (
    ChatResponse
)

from app.rag.rag_engine import (
    RAGEngine
)

router = APIRouter()

rag_engine = (
    RAGEngine()
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    result = (
        rag_engine.generate(
            request.message
        )
    )

    return ChatResponse(

        response=result[
            "response"
        ]
    )
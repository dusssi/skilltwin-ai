"""Knowledge-base transparency route (what the AI can retrieve)."""

from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import get_current_user
from app.knowledge.retriever import KnowledgeRetriever

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

retriever = KnowledgeRetriever()


@router.get("/search")
def search(q: str = Query(min_length=1, max_length=300),
           user: dict = Depends(get_current_user)):
    results = retriever.retrieve_many(q)
    return {"query": q, "results": [result.model_dump() for result in results]}

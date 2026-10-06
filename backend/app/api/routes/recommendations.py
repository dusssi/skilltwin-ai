"""Recommendation routes."""

from fastapi import APIRouter, Depends, Query

from app.api.errors import not_found
from app.api.schemas.requests import RecommendationStatusRequest
from app.auth.dependencies import get_current_user
from app.db import content as content_repo
from app.recommendations.engine import RecommendationEngine

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

engine = RecommendationEngine()


@router.get("")
def list_recommendations(
    status: str | None = Query(default=None, max_length=16),
    user: dict = Depends(get_current_user),
):
    return {"recommendations": content_repo.list_recommendations(user["id"], status=status)}


@router.post("/generate", status_code=201)
def generate(user: dict = Depends(get_current_user)):
    return engine.generate(user["id"])


@router.patch("/{rec_id}")
def update_status(rec_id: int, payload: RecommendationStatusRequest,
                  user: dict = Depends(get_current_user)):
    record = content_repo.update_recommendation_status(user["id"], rec_id, payload.status)
    if not record:
        raise not_found("Recommendation")
    return record

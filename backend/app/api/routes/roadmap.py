"""Roadmap routes: active roadmap, generation, item completion."""

from fastapi import APIRouter, Depends

from app.api.errors import not_found
from app.api.schemas.requests import RoadmapGenerateRequest, RoadmapItemUpdateRequest
from app.auth.dependencies import get_current_user
from app.db import content as content_repo
from app.roadmap.service import RoadmapService

router = APIRouter(prefix="/roadmap", tags=["roadmap"])

service = RoadmapService()


@router.get("")
def get_roadmap(user: dict = Depends(get_current_user)):
    active = service.get_active(user["id"])
    if not active:
        return {"roadmap": None, "items": [], "progress": {"total": 0, "completed": 0, "percent": 0}}
    return active


@router.get("/history")
def roadmap_history(user: dict = Depends(get_current_user)):
    return {"roadmaps": content_repo.list_roadmaps(user["id"])}


@router.post("/generate", status_code=201)
def generate_roadmap(payload: RoadmapGenerateRequest, user: dict = Depends(get_current_user)):
    generated = service.generate(user["id"], goal=payload.goal)
    items = generated["items"]
    done = sum(1 for item in items if item["status"] == "completed")
    return {
        "roadmap": generated["roadmap"],
        "items": items,
        "progress": {"total": len(items), "completed": done,
                     "percent": round(done / len(items) * 100) if items else 0},
    }


@router.patch("/items/{item_id}")
def update_item(item_id: int, payload: RoadmapItemUpdateRequest,
                user: dict = Depends(get_current_user)):
    if payload.status == "completed":
        try:
            return service.complete_item(user["id"], item_id)
        except LookupError:
            raise not_found("Roadmap item")
    item = content_repo.update_roadmap_item(user["id"], item_id, {"status": payload.status})
    if not item:
        raise not_found("Roadmap item")
    return {"item": item}

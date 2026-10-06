"""Memory routes: long-term memories and progress events."""

from fastapi import APIRouter, Depends, Query

from app.api.schemas.requests import MemoryCreateRequest
from app.auth.dependencies import get_current_user
from app.db import memory as memory_repo
from app.memory.memory_manager import MemoryManager

router = APIRouter(prefix="/memory", tags=["memory"])

manager = MemoryManager()


@router.get("")
def list_memory(
    kind: str | None = Query(default=None, max_length=32),
    q: str | None = Query(default=None, max_length=200),
    user: dict = Depends(get_current_user),
):
    if q:
        keywords = [part for part in q.replace(",", " ").split() if part]
        return {"memories": manager.recall(user["id"], keywords=keywords, limit=20)}
    return {"memories": manager.list_memories(user["id"], kind=kind)}


@router.post("", status_code=201)
def create_memory(payload: MemoryCreateRequest, user: dict = Depends(get_current_user)):
    return manager.remember(user["id"], payload.kind, payload.content, payload.importance)


@router.get("/events")
def list_events(
    event_type: str | None = Query(default=None, max_length=64),
    user: dict = Depends(get_current_user),
):
    return {"events": memory_repo.list_events(user["id"], event_type=event_type)}

"""Skill Twin routes: twin view, profile, skills, gaps, goals, projects."""

from fastapi import APIRouter, Depends

from app.api.errors import bad_request, not_found
from app.api.schemas.requests import (
    GoalCreateRequest,
    GoalUpdateRequest,
    ProjectCreateRequest,
    SkillAddRequest,
    TwinUpdateRequest,
)
from app.auth.dependencies import get_current_user
from app.db import memory as memory_repo
from app.db import twin as twin_repo
from app.twin import service as twin_service

router = APIRouter(prefix="/twin", tags=["twin"])


@router.get("")
def get_twin(user: dict = Depends(get_current_user)):
    return twin_service.full_twin(user["id"])


@router.get("/summary")
def get_summary(user: dict = Depends(get_current_user)):
    return twin_service.build_summary(user["id"]).model_dump()


@router.patch("")
def update_twin(payload: TwinUpdateRequest, user: dict = Depends(get_current_user)):
    fields = payload.model_dump(exclude_none=True)
    if "target_role" in fields and fields["target_role"]:
        twin_service.set_target_role(user["id"], fields.pop("target_role"))
    if fields:
        twin_repo.update_profile(user["id"], fields)
    if "primary_goal" in (payload.model_dump(exclude_none=True) or {}):
        memory_repo.record_event(
            user["id"], "career_goal_changed",
            data={"goal": payload.primary_goal, "via": "twin_update"},
        )
    return twin_service.full_twin(user["id"])


@router.get("/skills")
def list_skills(user: dict = Depends(get_current_user)):
    return {"skills": twin_repo.list_user_skills(user["id"])}


@router.post("/skills", status_code=201)
def add_skill(payload: SkillAddRequest, user: dict = Depends(get_current_user)):
    change = twin_service.add_skill_evidence(
        user_id=user["id"],
        skill_name=payload.name,
        source="manual",
        note=payload.note or "Added manually",
        level_hint=payload.level,
    )
    return change


@router.get("/skills/history")
def skill_history(user: dict = Depends(get_current_user)):
    return {"history": twin_repo.list_skill_history(user["id"])}


@router.get("/gaps")
def get_gaps(user: dict = Depends(get_current_user)):
    gaps, role_key = twin_service.get_gaps(user["id"], persist=True)
    return {"role_key": role_key, "gaps": [gap.model_dump() for gap in gaps]}


@router.get("/goals")
def list_goals(user: dict = Depends(get_current_user)):
    return {"goals": twin_repo.list_goals(user["id"])}


@router.post("/goals", status_code=201)
def create_goal(payload: GoalCreateRequest, user: dict = Depends(get_current_user)):
    goal = twin_repo.create_goal(user["id"], payload.title, payload.target_role)
    memory_repo.record_event(user["id"], "career_goal_changed",
                             ref_type="goal", ref_id=str(goal["id"]),
                             data={"goal": payload.title})
    return goal


@router.patch("/goals/{goal_id}")
def update_goal(goal_id: int, payload: GoalUpdateRequest, user: dict = Depends(get_current_user)):
    goal = twin_repo.update_goal(user["id"], goal_id, payload.model_dump(exclude_none=True))
    if not goal:
        raise not_found("Goal")
    return goal


@router.get("/projects")
def list_projects(user: dict = Depends(get_current_user)):
    return {"projects": twin_repo.list_projects(user["id"])}


@router.post("/projects", status_code=201)
def create_project(payload: ProjectCreateRequest, user: dict = Depends(get_current_user)):
    project = twin_repo.create_project(
        user["id"], payload.title, payload.description, payload.skills, payload.status
    )
    if payload.status == "completed":
        for skill_name in payload.skills:
            twin_service.add_skill_evidence(
                user["id"], skill_name, source="project",
                note=f"Project completed: {payload.title}",
            )
        memory_repo.record_event(user["id"], "project_completed",
                                 ref_type="project", ref_id=str(project["id"]),
                                 data={"title": payload.title})
    return project

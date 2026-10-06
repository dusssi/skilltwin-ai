"""Authentication routes: register, login, me, logout."""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlite3 import IntegrityError

from app.api.errors import bad_request, conflict, unauthorized
from app.api.schemas.requests import LoginRequest, RegisterRequest
from app.auth.dependencies import get_current_user
from app.auth.security import hash_password, issue_token, revoke_token, verify_password
from app.config.settings import settings
from app.db import users as user_repo
from app.twin import service as twin_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(payload: RegisterRequest):
    if len(payload.password) < settings.PASSWORD_MIN_LENGTH:
        raise bad_request(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters.")
    if user_repo.get_user_by_username(payload.username):
        raise conflict("Username is already taken.")
    try:
        user = user_repo.create_user(
            username=payload.username,
            display_name=payload.display_name or payload.username,
            password_hash=hash_password(payload.password),
        )
    except IntegrityError:
        raise conflict("Username is already taken.")
    token = issue_token(user["id"])
    return {"user": user, "token": token["token"], "expires_at": token["expires_at"]}


@router.post("/login")
def login(payload: LoginRequest):
    credentials = user_repo.get_user_credentials(payload.username)
    if not credentials or not verify_password(payload.password, credentials["password_hash"]):
        raise unauthorized("Invalid username or password.")
    user = user_repo.get_user_by_id(credentials["id"])
    token = issue_token(user["id"])
    return {"user": user, "token": token["token"], "expires_at": token["expires_at"]}


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return {"user": user, "twin_summary": twin_service.build_summary(user["id"]).model_dump()}


@router.post("/logout")
def logout(
    user: dict = Depends(get_current_user),
    credentials=Depends(__import__("app.auth.dependencies", fromlist=["_bearer_scheme"])._bearer_scheme),
):
    if credentials is not None and credentials.credentials:
        revoke_token(credentials.credentials)
    return {"status": "ok"}

"""FastAPI dependencies for authenticated, user-isolated access."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.errors import unauthorized
from app.auth.security import resolve_token

_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> dict:
    if credentials is None or not credentials.credentials:
        raise unauthorized("Missing bearer token.")
    user = resolve_token(credentials.credentials)
    if user is None:
        raise unauthorized("Invalid or expired token.")
    return user

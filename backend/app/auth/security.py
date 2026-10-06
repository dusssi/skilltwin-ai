"""Password hashing and opaque bearer-token management (stdlib only)."""

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timezone

from app.db import users as user_repo

_HASH_ITERATIONS = 210_000
_SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = os.urandom(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _HASH_ITERATIONS
    )
    return f"pbkdf2${_HASH_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, iterations, salt_hex, hash_hex = stored.split("$", 3)
        if scheme != "pbkdf2":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), hash_hex)
    except (ValueError, TypeError):
        return False


def issue_token(user_id: str) -> dict:
    token = secrets.token_urlsafe(32)
    return user_repo.create_token(user_id, token)


def resolve_token(token: str) -> dict | None:
    """Return the user for a valid, unexpired token, else None."""
    record = user_repo.get_token(token)
    if not record:
        return None
    try:
        expires_at = datetime.fromisoformat(record["expires_at"])
    except ValueError:
        return None
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        user_repo.delete_token(token)
        return None
    return user_repo.get_user_by_id(record["user_id"])


def revoke_token(token: str) -> None:
    user_repo.delete_token(token)

"""User and auth-token persistence."""

import uuid
from datetime import datetime, timedelta, timezone

from app.config.settings import settings
from app.db.database import transaction, utcnow


def _new_id() -> str:
    return uuid.uuid4().hex


def create_user(username: str, display_name: str, password_hash: str) -> dict:
    user_id = _new_id()
    now = utcnow()
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO users (id, username, display_name, password_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, display_name or username, password_hash, now, now),
        )
        conn.execute(
            """
            INSERT INTO profiles (user_id, display_name, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, display_name or username, now, now),
        )
    return get_user_by_id(user_id)


def get_user_by_username(username: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, username, display_name, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None


def get_user_credentials(username: str) -> dict | None:
    """Return id + password hash for login verification (internal use only)."""
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, username, display_name, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None


def create_token(user_id: str, token: str) -> dict:
    now = datetime.now(timezone.utc)
    expires_at = (now + timedelta(hours=settings.TOKEN_EXPIRE_HOURS)).isoformat()
    with transaction() as conn:
        conn.execute(
            "INSERT INTO auth_tokens (token, user_id, expires_at, created_at) VALUES (?, ?, ?, ?)",
            (token, user_id, expires_at, now.isoformat()),
        )
    return {"token": token, "user_id": user_id, "expires_at": expires_at}


def get_token(token: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT token, user_id, expires_at FROM auth_tokens WHERE token = ?",
            (token,),
        ).fetchone()
        return dict(row) if row else None


def delete_token(token: str) -> None:
    with transaction() as conn:
        conn.execute("DELETE FROM auth_tokens WHERE token = ?", (token,))


def delete_expired_tokens() -> int:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute("DELETE FROM auth_tokens WHERE expires_at < ?", (now,))
        return cursor.rowcount

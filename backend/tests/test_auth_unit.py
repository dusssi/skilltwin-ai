"""Unit tests for password hashing and token lifecycle."""

from datetime import datetime, timedelta, timezone

from app.auth.security import hash_password, issue_token, resolve_token, revoke_token, verify_password
from app.db import users as user_repo


def test_password_roundtrip():
    hashed = hash_password("correct horse battery")
    assert verify_password("correct horse battery", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_hash_format_and_salt_uniqueness():
    first, second = hash_password("same"), hash_password("same")
    assert first != second  # random salt
    assert first.startswith("pbkdf2$")


def test_malformed_hash_rejected():
    assert verify_password("x", "not-a-hash") is False
    assert verify_password("x", "") is False


def test_token_issue_resolve_revoke(tmp_env):
    user = user_repo.create_user("tu", "TU", hash_password("password123"))
    token = issue_token(user["id"])
    assert resolve_token(token["token"])["id"] == user["id"]
    revoke_token(token["token"])
    assert resolve_token(token["token"]) is None


def test_expired_token_rejected(tmp_env):
    from app.db.database import transaction

    user = user_repo.create_user("te", "TE", hash_password("password123"))
    token = issue_token(user["id"])
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    with transaction() as conn:
        conn.execute("UPDATE auth_tokens SET expires_at = ? WHERE token = ?",
                     (past, token["token"]))
    assert resolve_token(token["token"]) is None


def test_unknown_token_rejected(tmp_env):
    assert resolve_token("nope") is None

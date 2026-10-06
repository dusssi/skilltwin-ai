"""Memories, progress events, sessions and messages persistence."""

import json
import uuid

from app.db.database import transaction, utcnow


def _loads(value, default):
    if not value:
        return default
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------- memories
def create_memory(user_id: str, kind: str, content: str, importance: int = 5) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO memories (user_id, kind, content, importance, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, kind, content, max(1, min(10, int(importance))), now, now),
        )
        memory_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM memories WHERE id = ?", (memory_id,)).fetchone()
        return dict(row)


def list_memories(user_id: str, kind: str | None = None, limit: int = 100) -> list:
    with transaction() as conn:
        if kind:
            rows = conn.execute(
                "SELECT * FROM memories WHERE user_id = ? AND kind = ?"
                " ORDER BY importance DESC, id DESC LIMIT ?",
                (user_id, kind, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM memories WHERE user_id = ?"
                " ORDER BY importance DESC, id DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        return [dict(row) for row in rows]


def search_memories(user_id: str, keywords: list, limit: int = 10) -> list:
    """Keyword-overlap retrieval over long-term memories (case-insensitive)."""
    memories = list_memories(user_id, limit=500)
    if not keywords:
        return memories[:limit]
    lowered = [k.lower() for k in keywords if k]
    scored = []
    for memory in memories:
        text = f"{memory['kind']} {memory['content']}".lower()
        score = sum(1 for keyword in lowered if keyword in text)
        if score:
            scored.append((score + memory["importance"] / 10.0, memory))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [memory for _, memory in scored[:limit]]


# ---------------------------------------------------------------- progress events
def record_event(
    user_id: str,
    event_type: str,
    ref_type: str = "",
    ref_id: str = "",
    data: dict | None = None,
) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO progress_events (user_id, event_type, ref_type, ref_id, data, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, event_type, ref_type or "", str(ref_id or ""), json.dumps(data or {}), now),
        )
        event_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM progress_events WHERE id = ?", (event_id,)).fetchone()
        record = dict(row)
        record["data"] = _loads(record["data"], {})
        return record


def list_events(user_id: str, event_type: str | None = None, limit: int = 100) -> list:
    with transaction() as conn:
        if event_type:
            rows = conn.execute(
                "SELECT * FROM progress_events WHERE user_id = ? AND event_type = ?"
                " ORDER BY id DESC LIMIT ?",
                (user_id, event_type, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM progress_events WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        items = []
        for row in rows:
            record = dict(row)
            record["data"] = _loads(record["data"], {})
            items.append(record)
        return items


# ---------------------------------------------------------------- sessions & messages
def create_session(user_id: str) -> dict:
    session_id = uuid.uuid4().hex
    now = utcnow()
    with transaction() as conn:
        conn.execute(
            "INSERT INTO sessions (id, user_id, summary, created_at, updated_at)"
            " VALUES (?, ?, '', ?, ?)",
            (session_id, user_id, now, now),
        )
        row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        return dict(row)


def get_session(user_id: str, session_id: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id = ? AND user_id = ?", (session_id, user_id)
        ).fetchone()
        return dict(row) if row else None


def list_sessions(user_id: str, limit: int = 20) -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE user_id = ? ORDER BY updated_at DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict(row) for row in rows]


def update_session_summary(user_id: str, session_id: str, summary: str) -> None:
    with transaction() as conn:
        conn.execute(
            "UPDATE sessions SET summary = ?, updated_at = ? WHERE id = ? AND user_id = ?",
            (summary, utcnow(), session_id, user_id),
        )


def add_message(user_id: str, session_id: str, role: str, content: str) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO messages (session_id, user_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, user_id, role, content, now),
        )
        message_id = cursor.lastrowid
        conn.execute(
            "UPDATE sessions SET updated_at = ? WHERE id = ? AND user_id = ?",
            (now, session_id, user_id),
        )
        row = conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
        return dict(row)


def list_messages(user_id: str, session_id: str, limit: int = 50) -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT * FROM messages WHERE session_id = ? AND user_id = ?"
            " ORDER BY id ASC LIMIT ?",
            (session_id, user_id, limit),
        ).fetchall()
        return [dict(row) for row in rows]

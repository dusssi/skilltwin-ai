"""Skill Twin persistence: profiles, goals, projects, skills, history, gaps."""

import json

from app.db.database import transaction, utcnow


def _loads(value, default):
    if not value:
        return default
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------- profiles
def get_profile(user_id: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            """
            SELECT user_id, display_name, target_role, primary_goal,
                   experience_years, education, preferences, created_at, updated_at
            FROM profiles WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        if not row:
            return None
        profile = dict(row)
        profile["preferences"] = _loads(profile["preferences"], {})
        return profile


def update_profile(user_id: str, fields: dict) -> dict | None:
    allowed = {
        "display_name",
        "target_role",
        "primary_goal",
        "experience_years",
        "education",
        "preferences",
    }
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if "preferences" in updates and isinstance(updates["preferences"], dict):
        updates["preferences"] = json.dumps(updates["preferences"])
    if not updates:
        return get_profile(user_id)
    updates["updated_at"] = utcnow()
    columns = ", ".join(f"{key} = ?" for key in updates)
    with transaction() as conn:
        conn.execute(
            f"UPDATE profiles SET {columns} WHERE user_id = ?",
            (*updates.values(), user_id),
        )
    return get_profile(user_id)


# ---------------------------------------------------------------- career goals
def list_goals(user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            """
            SELECT id, user_id, title, target_role, status, created_at, updated_at
            FROM career_goals WHERE user_id = ? ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def create_goal(user_id: str, title: str, target_role: str = "") -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO career_goals (user_id, title, target_role, status, created_at, updated_at)
            VALUES (?, ?, ?, 'active', ?, ?)
            """,
            (user_id, title, target_role or "", now, now),
        )
        goal_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, user_id, title, target_role, status, created_at, updated_at"
            " FROM career_goals WHERE id = ?",
            (goal_id,),
        ).fetchone()
        return dict(row)


def update_goal(user_id: str, goal_id: int, fields: dict) -> dict | None:
    allowed = {"title", "target_role", "status"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not updates:
        return get_goal(user_id, goal_id)
    updates["updated_at"] = utcnow()
    columns = ", ".join(f"{key} = ?" for key in updates)
    with transaction() as conn:
        conn.execute(
            f"UPDATE career_goals SET {columns} WHERE id = ? AND user_id = ?",
            (*updates.values(), goal_id, user_id),
        )
    return get_goal(user_id, goal_id)


def get_goal(user_id: str, goal_id: int) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, user_id, title, target_role, status, created_at, updated_at"
            " FROM career_goals WHERE id = ? AND user_id = ?",
            (goal_id, user_id),
        ).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------- projects
def list_projects(user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            """
            SELECT id, user_id, title, description, skills, status, created_at, updated_at
            FROM projects WHERE user_id = ? ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()
        items = []
        for row in rows:
            item = dict(row)
            item["skills"] = _loads(item["skills"], [])
            items.append(item)
        return items


def create_project(
    user_id: str,
    title: str,
    description: str = "",
    skills: list | None = None,
    status: str = "planned",
) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO projects (user_id, title, description, skills, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, description or "", json.dumps(skills or []), status, now, now),
        )
        project_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, user_id, title, description, skills, status, created_at, updated_at"
            " FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        item = dict(row)
        item["skills"] = _loads(item["skills"], [])
        return item


def update_project(user_id: str, project_id: int, fields: dict) -> dict | None:
    allowed = {"title", "description", "skills", "status"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if "skills" in updates and isinstance(updates["skills"], list):
        updates["skills"] = json.dumps(updates["skills"])
    if not updates:
        return get_project(user_id, project_id)
    updates["updated_at"] = utcnow()
    columns = ", ".join(f"{key} = ?" for key in updates)
    with transaction() as conn:
        conn.execute(
            f"UPDATE projects SET {columns} WHERE id = ? AND user_id = ?",
            (*updates.values(), project_id, user_id),
        )
    return get_project(user_id, project_id)


def get_project(user_id: str, project_id: int) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, user_id, title, description, skills, status, created_at, updated_at"
            " FROM projects WHERE id = ? AND user_id = ?",
            (project_id, user_id),
        ).fetchone()
        if not row:
            return None
        item = dict(row)
        item["skills"] = _loads(item["skills"], [])
        return item


# ---------------------------------------------------------------- skill catalog
def ensure_skill(name: str, aliases: list | None = None, category: str = "") -> dict:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, name, aliases, category FROM skills WHERE name = ?", (name,)
        ).fetchone()
        if row:
            return dict(row)
        cursor = conn.execute(
            "INSERT INTO skills (name, aliases, category) VALUES (?, ?, ?)",
            (name, json.dumps(aliases or []), category or ""),
        )
        row = conn.execute(
            "SELECT id, name, aliases, category FROM skills WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
        item = dict(row)
        item["aliases"] = _loads(item["aliases"], [])
        return item


def get_skill_by_name(name: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, name, aliases, category FROM skills WHERE name = ?", (name,)
        ).fetchone()
        if not row:
            return None
        item = dict(row)
        item["aliases"] = _loads(item["aliases"], [])
        return item


def list_skills_catalog() -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT id, name, aliases, category FROM skills ORDER BY name"
        ).fetchall()
        items = []
        for row in rows:
            item = dict(row)
            item["aliases"] = _loads(item["aliases"], [])
            items.append(item)
        return items


# ---------------------------------------------------------------- user skills
def get_user_skill(user_id: str, skill_id: int) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            """
            SELECT us.user_id, us.skill_id, s.name AS skill_name, us.level,
                   us.target_level, us.confidence, us.evidence, us.updated_at
            FROM user_skills us JOIN skills s ON s.id = us.skill_id
            WHERE us.user_id = ? AND us.skill_id = ?
            """,
            (user_id, skill_id),
        ).fetchone()
        if not row:
            return None
        item = dict(row)
        item["evidence"] = _loads(item["evidence"], [])
        return item


def list_user_skills(user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            """
            SELECT us.user_id, us.skill_id, s.name AS skill_name, s.category,
                   us.level, us.target_level, us.confidence, us.evidence, us.updated_at
            FROM user_skills us JOIN skills s ON s.id = us.skill_id
            WHERE us.user_id = ? ORDER BY s.name
            """,
            (user_id,),
        ).fetchall()
        items = []
        for row in rows:
            item = dict(row)
            item["evidence"] = _loads(item["evidence"], [])
            items.append(item)
        return items


def upsert_user_skill(
    user_id: str,
    skill_id: int,
    level: int,
    target_level: int,
    confidence: float,
    evidence: list,
) -> dict:
    now = utcnow()
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO user_skills (user_id, skill_id, level, target_level, confidence, evidence, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, skill_id) DO UPDATE SET
                level = excluded.level,
                target_level = excluded.target_level,
                confidence = excluded.confidence,
                evidence = excluded.evidence,
                updated_at = excluded.updated_at
            """,
            (
                user_id,
                skill_id,
                max(1, min(5, int(level))),
                max(1, min(5, int(target_level))),
                max(0.0, min(1.0, float(confidence))),
                json.dumps(evidence),
                now,
            ),
        )
    return get_user_skill(user_id, skill_id)


def add_skill_history(
    user_id: str,
    skill_id: int,
    old_level: int,
    new_level: int,
    reason: str = "",
    source: str = "",
) -> None:
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO skill_history (user_id, skill_id, old_level, new_level, reason, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, skill_id, old_level, new_level, reason or "", source or "", utcnow()),
        )


def list_skill_history(user_id: str, limit: int = 100) -> list:
    with transaction() as conn:
        rows = conn.execute(
            """
            SELECT h.id, h.user_id, h.skill_id, s.name AS skill_name, h.old_level,
                   h.new_level, h.reason, h.source, h.created_at
            FROM skill_history h JOIN skills s ON s.id = h.skill_id
            WHERE h.user_id = ? ORDER BY h.id DESC LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(row) for row in rows]


# ---------------------------------------------------------------- gap snapshots
def save_gap_snapshot(user_id: str, gaps: list) -> None:
    now = utcnow()
    with transaction() as conn:
        conn.execute("DELETE FROM skill_gap_snapshots WHERE user_id = ?", (user_id,))
        for gap in gaps:
            conn.execute(
                """
                INSERT INTO skill_gap_snapshots
                    (user_id, skill_name, current_level, target_level, gap, priority, reason, recommended_action, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    gap["skill_name"],
                    gap["current_level"],
                    gap["target_level"],
                    gap["gap"],
                    gap["priority"],
                    gap.get("reason", ""),
                    gap.get("recommended_action", ""),
                    now,
                ),
            )


def list_gap_snapshot(user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            """
            SELECT id, user_id, skill_name, current_level, target_level, gap,
                   priority, reason, recommended_action, created_at
            FROM skill_gap_snapshots WHERE user_id = ? ORDER BY gap DESC, skill_name
            """,
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]

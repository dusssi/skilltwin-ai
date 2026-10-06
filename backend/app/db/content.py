"""Resumes, analyses, roadmaps, roadmap items and recommendations persistence."""

import json

from app.db.database import transaction, utcnow


def _loads(value, default):
    if not value:
        return default
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------- resumes
def create_resume(
    user_id: str, filename_stored: str, filename_original: str, content_text: str
) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO resumes (user_id, filename_stored, filename_original, content_text, uploaded_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, filename_stored, filename_original, content_text or "", now),
        )
        resume_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, user_id, filename_stored, filename_original, uploaded_at"
            " FROM resumes WHERE id = ?",
            (resume_id,),
        ).fetchone()
        return dict(row)


def list_resumes(user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            """
            SELECT id, user_id, filename_stored, filename_original, uploaded_at
            FROM resumes WHERE user_id = ? ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def save_resume_analysis(
    resume_id: int,
    user_id: str,
    extracted_skills: list,
    missing_skills: list,
    experience: dict,
    projects: list,
    education: list,
    career_signals: list,
    readiness_score: int,
) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO resume_analyses
                (resume_id, user_id, extracted_skills, missing_skills, experience,
                 projects, education, career_signals, readiness_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resume_id,
                user_id,
                json.dumps(extracted_skills),
                json.dumps(missing_skills),
                json.dumps(experience),
                json.dumps(projects),
                json.dumps(education),
                json.dumps(career_signals),
                int(readiness_score),
                now,
            ),
        )
        analysis_id = cursor.lastrowid
        row = conn.execute(
            "SELECT * FROM resume_analyses WHERE id = ?", (analysis_id,)
        ).fetchone()
        item = dict(row)
        item["extracted_skills"] = _loads(item["extracted_skills"], [])
        item["missing_skills"] = _loads(item["missing_skills"], [])
        item["experience"] = _loads(item["experience"], {})
        item["projects"] = _loads(item["projects"], [])
        item["education"] = _loads(item["education"], [])
        item["career_signals"] = _loads(item["career_signals"], [])
        return item


def list_resume_analyses(user_id: str, limit: int = 20) -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT * FROM resume_analyses WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        items = []
        for row in rows:
            item = dict(row)
            item["extracted_skills"] = _loads(item["extracted_skills"], [])
            item["missing_skills"] = _loads(item["missing_skills"], [])
            item["experience"] = _loads(item["experience"], {})
            item["projects"] = _loads(item["projects"], [])
            item["education"] = _loads(item["education"], [])
            item["career_signals"] = _loads(item["career_signals"], [])
            items.append(item)
        return items


# ---------------------------------------------------------------- roadmaps
def create_roadmap(user_id: str, goal: str) -> dict:
    now = utcnow()
    with transaction() as conn:
        conn.execute(
            "UPDATE roadmaps SET status = 'archived', updated_at = ?"
            " WHERE user_id = ? AND status = 'active'",
            (now, user_id),
        )
        cursor = conn.execute(
            "INSERT INTO roadmaps (user_id, goal, status, created_at, updated_at)"
            " VALUES (?, ?, 'active', ?, ?)",
            (user_id, goal or "", now, now),
        )
        roadmap_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, user_id, goal, status, created_at, updated_at FROM roadmaps WHERE id = ?",
            (roadmap_id,),
        ).fetchone()
        return dict(row)


def get_active_roadmap(user_id: str) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT id, user_id, goal, status, created_at, updated_at FROM roadmaps"
            " WHERE user_id = ? AND status = 'active' ORDER BY id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None


def list_roadmaps(user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT id, user_id, goal, status, created_at, updated_at FROM roadmaps"
            " WHERE user_id = ? ORDER BY id DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def create_roadmap_item(roadmap_id: int, user_id: str, item: dict) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO roadmap_items
                (roadmap_id, user_id, title, description, skill, difficulty,
                 estimated_effort, priority, status, dependencies, resources,
                 position, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                roadmap_id,
                user_id,
                item["title"],
                item.get("description", ""),
                item.get("skill", ""),
                item.get("difficulty", "beginner"),
                item.get("estimated_effort", ""),
                item.get("priority", "medium"),
                "pending",
                json.dumps(item.get("dependencies", [])),
                json.dumps(item.get("resources", [])),
                int(item.get("position", 0)),
                now,
                now,
            ),
        )
        item_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM roadmap_items WHERE id = ?", (item_id,)).fetchone()
        record = dict(row)
        record["dependencies"] = _loads(record["dependencies"], [])
        record["resources"] = _loads(record["resources"], [])
        return record


def list_roadmap_items(roadmap_id: int, user_id: str) -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT * FROM roadmap_items WHERE roadmap_id = ? AND user_id = ?"
            " ORDER BY position, id",
            (roadmap_id, user_id),
        ).fetchall()
        items = []
        for row in rows:
            record = dict(row)
            record["dependencies"] = _loads(record["dependencies"], [])
            record["resources"] = _loads(record["resources"], [])
            items.append(record)
        return items


def get_roadmap_item(user_id: str, item_id: int) -> dict | None:
    with transaction() as conn:
        row = conn.execute(
            "SELECT * FROM roadmap_items WHERE id = ? AND user_id = ?",
            (item_id, user_id),
        ).fetchone()
        if not row:
            return None
        record = dict(row)
        record["dependencies"] = _loads(record["dependencies"], [])
        record["resources"] = _loads(record["resources"], [])
        return record


def update_roadmap_item(user_id: str, item_id: int, fields: dict) -> dict | None:
    allowed = {"title", "description", "skill", "difficulty", "estimated_effort",
               "priority", "status", "dependencies", "resources"}
    updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if "dependencies" in updates and isinstance(updates["dependencies"], list):
        updates["dependencies"] = json.dumps(updates["dependencies"])
    if "resources" in updates and isinstance(updates["resources"], list):
        updates["resources"] = json.dumps(updates["resources"])
    if updates.get("status") == "completed":
        updates["completed_at"] = utcnow()
    if not updates:
        return get_roadmap_item(user_id, item_id)
    updates["updated_at"] = utcnow()
    columns = ", ".join(f"{key} = ?" for key in updates)
    with transaction() as conn:
        conn.execute(
            f"UPDATE roadmap_items SET {columns} WHERE id = ? AND user_id = ?",
            (*updates.values(), item_id, user_id),
        )
    return get_roadmap_item(user_id, item_id)


# ---------------------------------------------------------------- recommendations
def create_recommendation(user_id: str, kind: str, title: str, detail: dict) -> dict:
    now = utcnow()
    with transaction() as conn:
        cursor = conn.execute(
            """
            INSERT INTO recommendations (user_id, kind, title, detail, status, created_at)
            VALUES (?, ?, ?, ?, 'suggested', ?)
            """,
            (user_id, kind, title, json.dumps(detail or {}), now),
        )
        rec_id = cursor.lastrowid
        row = conn.execute(
            "SELECT * FROM recommendations WHERE id = ?", (rec_id,)
        ).fetchone()
        record = dict(row)
        record["detail"] = _loads(record["detail"], {})
        return record


def list_recommendations(user_id: str, status: str | None = None) -> list:
    with transaction() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM recommendations WHERE user_id = ? AND status = ?"
                " ORDER BY id DESC",
                (user_id, status),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM recommendations WHERE user_id = ? ORDER BY id DESC",
                (user_id,),
            ).fetchall()
        items = []
        for row in rows:
            record = dict(row)
            record["detail"] = _loads(record["detail"], {})
            items.append(record)
        return items


def update_recommendation_status(user_id: str, rec_id: int, status: str) -> dict | None:
    with transaction() as conn:
        conn.execute(
            "UPDATE recommendations SET status = ? WHERE id = ? AND user_id = ?",
            (status, rec_id, user_id),
        )
        row = conn.execute(
            "SELECT * FROM recommendations WHERE id = ? AND user_id = ?",
            (rec_id, user_id),
        ).fetchone()
        if not row:
            return None
        record = dict(row)
        record["detail"] = _loads(record["detail"], {})
        return record


def clear_suggested_recommendations(user_id: str, kinds: list | None = None) -> int:
    with transaction() as conn:
        if kinds:
            placeholders = ",".join("?" for _ in kinds)
            cursor = conn.execute(
                f"DELETE FROM recommendations WHERE user_id = ? AND status = 'suggested'"
                f" AND kind IN ({placeholders})",
                (user_id, *kinds),
            )
        else:
            cursor = conn.execute(
                "DELETE FROM recommendations WHERE user_id = ? AND status = 'suggested'",
                (user_id,),
            )
        return cursor.rowcount

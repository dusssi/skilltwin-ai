"""Unit tests for Twin merge/update logic (never blind overwrite)."""

from app.db import twin as twin_repo
from app.twin import service as twin_service


def test_first_evidence_creates_skill(tmp_env):
    from app.db import users as user_repo
    from app.auth.security import hash_password

    user = user_repo.create_user("u1", "U1", hash_password("password123"))
    change = twin_service.add_skill_evidence(user["id"], "Python", source="resume",
                                             note="resume #1")
    assert change["old_level"] == 0
    assert change["new_level"] >= 1
    assert change["leveled_up"] is True
    skills = twin_repo.list_user_skills(user["id"])
    assert len(skills) == 1
    assert skills[0]["evidence"][0]["source"] == "resume"


def test_evidence_appends_without_reset(tmp_env):
    from app.db import users as user_repo
    from app.auth.security import hash_password

    user = user_repo.create_user("u2", "U2", hash_password("password123"))
    twin_service.add_skill_evidence(user["id"], "Python", source="resume")
    twin_service.add_skill_evidence(user["id"], "Python", source="chat", note="mentioned")
    skills = twin_repo.list_user_skills(user["id"])
    assert len(skills) == 1  # merged, not duplicated
    assert len(skills[0]["evidence"]) == 2
    assert {e["source"] for e in skills[0]["evidence"]} == {"resume", "chat"}


def test_level_never_decreases(tmp_env):
    from app.db import users as user_repo
    from app.auth.security import hash_password

    user = user_repo.create_user("u3", "U3", hash_password("password123"))
    twin_service.add_skill_evidence(user["id"], "Python", source="roadmap", level_hint=4)
    twin_service.add_skill_evidence(user["id"], "Python", source="chat", level_hint=1)
    skill = twin_repo.list_user_skills(user["id"])[0]
    assert skill["level"] == 4


def test_level_changes_record_history(tmp_env):
    from app.db import users as user_repo
    from app.auth.security import hash_password

    user = user_repo.create_user("u4", "U4", hash_password("password123"))
    twin_service.add_skill_evidence(user["id"], "Python", source="resume")
    twin_service.add_skill_evidence(user["id"], "Python", source="roadmap", level_hint=4)
    history = twin_repo.list_skill_history(user["id"])
    assert len(history) >= 2
    assert history[0]["new_level"] == 4
    assert history[0]["source"] == "roadmap"


def test_target_role_refreshes_targets(tmp_env):
    from app.db import users as user_repo
    from app.auth.security import hash_password

    user = user_repo.create_user("u5", "U5", hash_password("password123"))
    twin_service.add_skill_evidence(user["id"], "React", source="manual")
    before = twin_repo.list_user_skills(user["id"])[0]["target_level"]
    twin_service.set_target_role(user["id"], "Frontend Developer")
    after = twin_repo.list_user_skills(user["id"])[0]["target_level"]
    assert after == 4
    assert before != after or before == 4

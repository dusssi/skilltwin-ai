"""DB-backed session manager (survives restarts, isolated per user)."""

from app.db import memory as memory_repo
from app.sessions.compressor import ContextCompressor


class SessionManager:
    def __init__(self):
        self.compressor = ContextCompressor()

    def create_session(self, user_id: str) -> dict:
        return memory_repo.create_session(user_id)

    def get_session(self, user_id: str, session_id: str) -> dict | None:
        return memory_repo.get_session(user_id, session_id)

    def list_sessions(self, user_id: str, limit: int = 20) -> list:
        return memory_repo.list_sessions(user_id, limit=limit)

    def add_message(self, user_id: str, session_id: str, role: str, content: str) -> dict:
        message = memory_repo.add_message(user_id, session_id, role, content)
        messages = memory_repo.list_messages(user_id, session_id, limit=100)
        summary = self.compressor.compress(messages)
        memory_repo.update_session_summary(user_id, session_id, summary)
        return message

    def recent_messages(self, user_id: str, session_id: str, limit: int = 12) -> list:
        messages = memory_repo.list_messages(user_id, session_id, limit=200)
        return messages[-limit:]

    def list_messages(self, user_id: str, session_id: str, limit: int = 50) -> list:
        return memory_repo.list_messages(user_id, session_id, limit=limit)

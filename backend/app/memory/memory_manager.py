"""Durable memory manager.

* Short-term memory: session messages (see ``app/sessions``).
* Long-term memory: ``memories`` rows (facts, goals, preferences,
  achievements, observations) + ``progress_events`` rows.
* Everything persists in SQLite and survives restarts.
* Retrieval is keyword-overlap ranked by importance/recency so memory
  actually influences chat context (see ``app/chat``).
"""

from app.db import memory as memory_repo


class MemoryManager:
    # ---------------------------------------------------------- long-term
    def remember(self, user_id: str, kind: str, content: str, importance: int = 5) -> dict:
        content = (content or "").strip()
        if not content:
            raise ValueError("Memory content is required.")
        return memory_repo.create_memory(user_id, kind or "fact", content, importance)

    def recall(self, user_id: str, keywords: list | None = None, limit: int = 10) -> list:
        if keywords:
            return memory_repo.search_memories(user_id, keywords, limit=limit)
        return memory_repo.list_memories(user_id, limit=limit)

    def list_memories(self, user_id: str, kind: str | None = None, limit: int = 100) -> list:
        return memory_repo.list_memories(user_id, kind=kind, limit=limit)

    # ------------------------------------------------------------- events
    def record_event(self, user_id: str, event_type: str, data: dict | None = None,
                     ref_type: str = "", ref_id: str = "") -> dict:
        return memory_repo.record_event(user_id, event_type, ref_type, ref_id, data or {})

    def recent_events(self, user_id: str, limit: int = 20) -> list:
        return memory_repo.list_events(user_id, limit=limit)

    def completed_tasks(self, user_id: str) -> list:
        events = memory_repo.list_events(user_id, event_type="roadmap_item_completed", limit=200)
        tasks = []
        for event in events:
            title = (event.get("data") or {}).get("title")
            if title:
                tasks.append(title)
        return tasks

    # ------------------------------------------------- context rendering
    def render_context(self, user_id: str, keywords: list | None = None, limit: int = 8) -> str:
        memories = self.recall(user_id, keywords=keywords, limit=limit)
        if not memories:
            return ""
        lines = [f"- [{memory['kind']}] {memory['content']}" for memory in memories]
        return "\n".join(lines)

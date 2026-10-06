"""Context engine: retrieve → rank → summarize over user memory."""

from app.context.ranking import ContextRanker
from app.context.retriever import ContextRetriever
from app.context.summarizer import ContextSummarizer
from app.memory.memory_manager import MemoryManager
from app.sessions.session_manager import SessionManager


class ContextEngine:
    def __init__(self):
        self.retriever = ContextRetriever()
        self.ranker = ContextRanker()
        self.summarizer = ContextSummarizer()
        self.memory = MemoryManager()
        self.sessions = SessionManager()

    def get_context(self, user_id: str, query: str, session_id: str | None = None) -> str:
        """Assemble relevant past context for a query (may be empty)."""
        candidates: list = []
        for memory in self.memory.recall(user_id, limit=100):
            candidates.append(f"[{memory['kind']}] {memory['content']}")
        if session_id:
            for message in self.sessions.recent_messages(user_id, session_id, limit=20):
                candidates.append(f"{message['role']}: {message['content']}")
        scored = self.retriever.retrieve(query, candidates, limit=10)
        ranked = self.ranker.rank(scored)
        return self.summarizer.summarize(ranked)

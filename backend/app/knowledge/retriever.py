"""TF-IDF knowledge retrieval with a relevance threshold.

Pure-Python implementation (no model downloads, deterministic, testable).
Queries scoring below ``settings.RAG_SIMILARITY_THRESHOLD`` return no
result instead of a random topic.
"""

import math
import re
from collections import Counter

from app.config.settings import settings
from app.knowledge.knowledge_store import KnowledgeStore
from app.knowledge.models import RetrievalResult


def _tokenize(text: str) -> list:
    return re.findall(r"[a-z0-9+#.]+", text.lower())


class KnowledgeRetriever:
    def __init__(self, store: KnowledgeStore | None = None):
        self.store = store or KnowledgeStore()
        self._idf: dict = {}
        self._doc_vectors: list = []
        self._build_index()

    def _build_index(self) -> None:
        items = self.store.get_all_items()
        doc_tokens = []
        doc_freq: Counter = Counter()
        for item in items:
            tokens = _tokenize(item.topic + " " + " ".join(item.facts))
            doc_tokens.append(tokens)
            for token in set(tokens):
                doc_freq[token] += 1
        total = max(1, len(items))
        self._idf = {
            token: math.log((1 + total) / (1 + freq)) + 1.0
            for token, freq in doc_freq.items()
        }
        self._doc_vectors = [self._vector(tokens) for tokens in doc_tokens]
        self._items = items

    def _vector(self, tokens: list) -> dict:
        counts = Counter(tokens)
        total = len(tokens) or 1
        return {
            token: (count / total) * self._idf.get(token, 1.0)
            for token, count in counts.items()
        }

    @staticmethod
    def _cosine(left: dict, right: dict) -> float:
        if not left or not right:
            return 0.0
        overlap = set(left) & set(right)
        numerator = sum(left[token] * right[token] for token in overlap)
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)

    def refresh(self) -> None:
        """Rebuild the index (call after adding documents)."""
        self._build_index()

    def retrieve(self, query: str, top_k: int | None = None) -> RetrievalResult | None:
        """Return the best matching document above threshold, else None."""
        if not query or not query.strip():
            return None
        query_vector = self._vector(_tokenize(query))
        best: RetrievalResult | None = None
        best_score = 0.0
        for item, vector in zip(self._items, self._doc_vectors):
            score = self._cosine(query_vector, vector)
            if score > best_score:
                best_score = score
                best = RetrievalResult(topic=item.topic, score=round(score, 4), facts=item.facts)
        threshold = settings.RAG_SIMILARITY_THRESHOLD
        if best is None or best_score < threshold:
            return None
        return best

    def retrieve_many(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:
        """Return up to top_k documents above threshold, best first."""
        limit = top_k or settings.RAG_TOP_K
        if not query or not query.strip():
            return []
        query_vector = self._vector(_tokenize(query))
        scored = []
        for item, vector in zip(self._items, self._doc_vectors):
            score = self._cosine(query_vector, vector)
            if score >= settings.RAG_SIMILARITY_THRESHOLD:
                scored.append(
                    RetrievalResult(topic=item.topic, score=round(score, 4), facts=item.facts)
                )
        scored.sort(key=lambda result: result.score, reverse=True)
        return scored[:limit]

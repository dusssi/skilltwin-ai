"""Relevance retrieval over session messages and long-term memories."""

import re


def _tokenize(text: str) -> set:
    return set(re.findall(r"[a-z0-9+#.]{3,}", (text or "").lower()))


class ContextRetriever:
    def retrieve(self, query: str, candidates: list, limit: int = 8) -> list:
        """Rank candidate texts by token overlap with the query.

        Candidates may be plain strings or dicts with a ``content`` key.
        Returns ``(score, text)`` pairs with score > 0, best first.
        """
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []
        scored = []
        for candidate in candidates:
            text = candidate.get("content", "") if isinstance(candidate, dict) else str(candidate)
            tokens = _tokenize(text)
            if not tokens:
                continue
            overlap = query_tokens & tokens
            if overlap:
                score = len(overlap) / max(1, len(query_tokens))
                scored.append((round(score, 4), text))
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[:limit]

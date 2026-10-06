"""Ranking of retrieved context candidates."""


class ContextRanker:
    def rank(self, scored: list, min_score: float = 0.1) -> list:
        """Filter by minimum relevance and order best-first.

        Accepts ``(score, text)`` pairs (new style) or plain strings
        (legacy style, kept for compatibility).
        """
        if not scored:
            return []
        if isinstance(scored[0], str):
            return sorted(scored, key=len, reverse=True)
        filtered = [(score, text) for score, text in scored if score >= min_score]
        filtered.sort(key=lambda item: item[0], reverse=True)
        return [text for _, text in filtered]

"""Context summarization with a stable character budget."""

MAX_CONTEXT_CHARS = 2000


class ContextSummarizer:
    def summarize(self, ranked_results: list, budget: int = MAX_CONTEXT_CHARS) -> str:
        if not ranked_results:
            return ""
        parts: list = []
        used = 0
        for text in ranked_results:
            text = str(text).strip()
            if not text:
                continue
            if used + len(text) + 3 > budget:
                remaining = budget - used - 3
                if remaining > 40:
                    parts.append(text[:remaining] + "…")
                break
            parts.append(text)
            used += len(text) + 3
        return "\n".join(f"- {part}" for part in parts)

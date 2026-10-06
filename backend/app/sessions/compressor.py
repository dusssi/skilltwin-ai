"""Deterministic conversation summarization (no LLM needed).

Keeps the opening goal plus the most recent exchanges, truncated to a
stable budget so session summaries are reproducible and testable.
"""

MAX_SUMMARY_CHARS = 800


class ContextCompressor:
    def compress(self, messages: list) -> str:
        texts = []
        for message in messages:
            if isinstance(message, dict):
                texts.append(f"{message.get('role', 'user')}: {message.get('content', '')}")
            else:
                texts.append(str(message))
        texts = [text.strip() for text in texts if text and text.strip()]
        if not texts:
            return ""
        if len(texts) <= 6:
            summary = " | ".join(texts)
        else:
            summary = texts[0] + " | ... | " + " | ".join(texts[-5:])
        if len(summary) > MAX_SUMMARY_CHARS:
            summary = summary[:MAX_SUMMARY_CHARS].rsplit(" ", 1)[0] + "…"
        return summary

"""File-backed knowledge store with runtime extension support."""

import json
from pathlib import Path

from app.knowledge.models import KnowledgeItem

_SEED_PATH = Path(__file__).with_name("seed.json")


class KnowledgeStore:
    """Loads the seed knowledge base; documents can be added at runtime."""

    def __init__(self, seed_path: Path | None = None):
        self._items: list[KnowledgeItem] = []
        self._load(seed_path or _SEED_PATH)

    def _load(self, path: Path) -> None:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raw = []
        for entry in raw:
            if isinstance(entry, dict) and entry.get("topic"):
                self._items.append(
                    KnowledgeItem(
                        topic=str(entry["topic"]),
                        facts=[str(fact) for fact in entry.get("facts", [])],
                    )
                )

    def get_all_items(self) -> list[KnowledgeItem]:
        return list(self._items)

    def add_document(self, topic: str, facts: list[str]) -> KnowledgeItem:
        item = KnowledgeItem(topic=topic, facts=list(facts))
        self._items.append(item)
        return item

"""Accurate skill extraction.

Fixes the legacy substring bug (``"c" in text`` matched almost everything)
with:

* case normalization,
* word-boundary aware regex matching,
* longest-match-first ordering so ``C++`` wins over ``C``,
* alias resolution through the shared skill catalog,
* non-overlapping span consumption so one text region yields one skill.
"""

import re

from app.twin.catalog import SKILL_CATALOG


def _pattern_for(term: str) -> str:
    """Build a boundary-aware pattern for a skill term or alias."""
    escaped = re.escape(term.strip())
    # Terms starting/ending with word chars get \b guards; symbol-heavy
    # terms (C++, C#, Node.js) use lookarounds instead.
    starts_word = term[0].isalnum() if term else False
    ends_word = term[-1].isalnum() if term else False
    prefix = r"\b" if starts_word else r"(?<![\w#+])"
    suffix = r"\b" if ends_word else r"(?![\w#+])"
    return prefix + escaped + suffix


class SkillExtractor:
    def __init__(self, catalog: list | None = None):
        self._matchers: list = []  # (compiled_regex, canonical_name, term_length)
        for entry in catalog or SKILL_CATALOG:
            name = entry["name"]
            terms = [name] + list(entry.get("aliases", []))
            for term in terms:
                if not term or not term.strip():
                    continue
                try:
                    regex = re.compile(_pattern_for(term), re.IGNORECASE)
                except re.error:
                    continue
                self._matchers.append((regex, name, len(term.strip())))
        # Longest terms first so "C++" claims its span before "C".
        self._matchers.sort(key=lambda item: item[2], reverse=True)

    def extract(self, text: str) -> list:
        """Return canonical skill names found in text (order of first mention)."""
        if not text:
            return []
        found: list = []
        seen: set = set()
        claimed: list = []  # non-overlapping (start, end) spans

        def _overlaps(start: int, end: int) -> bool:
            return any(start < stop and end > begin for begin, stop in claimed)

        # Collect earliest match position per skill for stable ordering.
        positions: dict = {}
        for regex, canonical, _ in self._matchers:
            for match in regex.finditer(text):
                start, end = match.span()
                if _overlaps(start, end):
                    continue
                claimed.append((start, end))
                if canonical not in seen:
                    seen.add(canonical)
                    positions[canonical] = start
                break  # one span per term is enough; other aliases may still match
        for canonical in sorted(positions, key=positions.get):
            found.append(canonical)
        return found

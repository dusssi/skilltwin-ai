"""Reflection agent: scores progress from real Twin deltas.

Score (0-10) combines gap closure, roadmap completion and skill growth —
computed transparently from typed input, with an optional LLM narrative.
"""

from app.llm.prompt_manager import PromptManager
from app.llm.provider import LLMProvider, LLMUnavailableError
from app.reflection.models import ReflectionInput, ReflectionResult


class Reflector:
    def __init__(self, provider: LLMProvider | None = None):
        self.provider = provider or LLMProvider()
        self.prompts = PromptManager()

    def reflect(self, reflection_input: ReflectionInput) -> ReflectionResult:
        data = reflection_input
        issues: list[str] = []
        suggestions: list[str] = []

        total_gaps = data.gaps_closed + data.gaps_open
        gap_score = (data.gaps_closed / total_gaps) if total_gaps else 1.0
        roadmap_score = (data.roadmap_completed / data.roadmap_total) if data.roadmap_total else 0.5
        growth_score = min(1.0, len(data.skills_improved) / 3)

        score = int(round((0.45 * gap_score + 0.35 * roadmap_score + 0.2 * growth_score) * 10))
        score = max(0, min(10, score))

        if data.gaps_open:
            issues.append(f"{data.gaps_open} skill gap(s) still open")
            suggestions.append("Attack the highest-priority gap with a focused learning block.")
        if data.roadmap_total and data.roadmap_completed < data.roadmap_total:
            remaining = data.roadmap_total - data.roadmap_completed
            issues.append(f"{remaining} roadmap item(s) pending")
            suggestions.append("Complete the next roadmap item to convert learning into evidence.")
        if not data.skills_improved:
            issues.append("No skill improvements recorded recently")
            suggestions.append("Finish one small task and log it so the Twin can record evidence.")
        else:
            suggestions.append(
                f"Keep momentum on: {', '.join(data.skills_improved[:3])}."
            )
        if not issues:
            suggestions.append("Set a stretch goal to keep growing.")

        narrative = self._narrative(data, score)
        return ReflectionResult(issues=issues, suggestions=suggestions, score=score,
                                narrative=narrative)

    def _narrative(self, data: ReflectionInput, score: int) -> str:
        fallback = (
            f"Progress score {score}/10: {data.gaps_closed} gap(s) closed, "
            f"{data.gaps_open} open; roadmap {data.roadmap_completed}/"
            f"{data.roadmap_total} complete."
        )
        if not self.provider.configured:
            return fallback
        try:
            prompt = self.prompts.build_reflection_prompt(
                twin_context=(
                    f"Goal: {data.goal}; gaps closed: {data.gaps_closed}; "
                    f"gaps open: {data.gaps_open}; improved: "
                    f"{', '.join(data.skills_improved) or 'none'}."
                ),
                recent_activity="; ".join(data.recent_events) or "no recent activity",
            )
            response = self.provider.generate(prompt, max_output_tokens=256)
            return response.content.strip() or fallback
        except LLMUnavailableError:
            return fallback

"""Personalized chat: every response is grounded in the user's Skill Twin.

Pipeline::

    user message
        → Twin context (skills/levels, gaps, goal, progress)
        → memory context (long-term recall + relevant past context)
        → knowledge context (threshold-gated retrieval)
        → conversation context (recent session messages)
        → LLM (or honest Twin-derived fallback when unavailable)
        → persist conversation + extract durable facts → Twin update

Two different users asking the same question receive different answers
because the Twin context differs.
"""

import re

from app.context.engine import ContextEngine
from app.db import memory as memory_repo
from app.db import twin as twin_repo
from app.knowledge.retriever import KnowledgeRetriever
from app.llm.models import ChatTwinUpdate
from app.llm.prompt_manager import SYSTEM_PROMPT, PromptManager
from app.llm.provider import LLMProvider, LLMUnavailableError
from app.llm.response_parser import ResponseParser
from app.memory.memory_manager import MemoryManager
from app.resume.extractor import SkillExtractor
from app.sessions.session_manager import SessionManager
from app.twin import service as twin_service

_GOAL_PATTERNS = [
    r"(?:my goal is|i want to become|i want to be|aiming for|targeting|my target role is)\s+([^.\n]{3,120})",
]
_DONE_PATTERNS = [
    r"(?:i (?:just )?completed|i finished|i built|i deployed|done with)\s+([^.\n]{3,160})",
]
_PREF_PATTERNS = [
    r"(?:i prefer|i like|i enjoy)\s+([^.\n]{3,160})",
]


class FallbackComposer:
    """Honest local responder used only when the LLM is unavailable.

    Output is explicitly labeled and derived entirely from the user's real
    Twin state — never presented as model output.
    """

    def compose(self, user_message: str, twin_summary, gaps: list, memories: str) -> str:
        lines = [
            "_Note: the AI model is currently unavailable, so here is guidance "
            "generated directly from your Skill Twin._",
            "",
            f"Your goal: **{twin_summary.primary_goal or 'not set yet'}** "
            f"→ target role **{twin_summary.target_role or 'not set yet'}**.",
        ]
        if gaps:
            lines.append("")
            lines.append("Your top skill gaps right now:")
            for gap in gaps[:5]:
                lines.append(
                    f"- **{gap.skill_name}**: {gap.current_level}/5 → "
                    f"{gap.target_level}/5 ({gap.priority} priority). {gap.reason}"
                )
            lines.append("")
            lines.append(
                f"Suggested next step: {gaps[0].recommended_action} "
                f"Start with '{gaps[0].skill_name}'."
            )
        else:
            lines.append("")
            lines.append(
                "No open gaps against your target role. Consider a stretch goal "
                "or a portfolio project to deepen your strongest skills."
            )
        if twin_summary.roadmap_progress:
            progress = twin_summary.roadmap_progress
            lines.append("")
            lines.append(
                f"Roadmap progress: {progress.get('completed', 0)}/"
                f"{progress.get('total', 0)} items "
                f"({progress.get('percent', 0)}%)."
            )
        if memories:
            lines.append("")
            lines.append("What I remember about you:")
            lines.append(memories)
        lines.append("")
        lines.append(f"Regarding your question — _{user_message[:200]}_ — tell me which "
                     "gap you want to attack first and I will break it into steps.")
        return "\n".join(lines)


class ChatService:
    def __init__(self, provider: LLMProvider | None = None):
        self.provider = provider or LLMProvider()
        self.prompts = PromptManager()
        self.parser = ResponseParser()
        self.sessions = SessionManager()
        self.memory = MemoryManager()
        self.context_engine = ContextEngine()
        self.knowledge = KnowledgeRetriever()
        self.extractor = SkillExtractor()
        self.fallback = FallbackComposer()

    # ------------------------------------------------------------------ chat
    def chat(self, user_id: str, message: str, session_id: str | None = None) -> dict:
        message = (message or "").strip()
        if not message:
            raise ValueError("Message is required.")
        session = self._resolve_session(user_id, session_id)
        session_id = session["id"]

        twin_summary = twin_service.build_summary(user_id)
        gaps, _ = twin_service.get_gaps(user_id, persist=False)
        keywords = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]{2,}", message)

        twin_context = self._render_twin_context(twin_summary, gaps)
        memory_context = self.memory.render_context(user_id, keywords=keywords, limit=8)
        past_context = self.context_engine.get_context(user_id, message, session_id)
        if past_context:
            memory_context = f"{memory_context}\n{past_context}".strip()
        knowledge_context = self._render_knowledge(message)
        conversation_context = self._render_conversation(user_id, session_id)

        prompt = self.prompts.build_chat_prompt(
            user_message=message,
            twin_context=twin_context,
            memory_context=memory_context,
            knowledge_context=knowledge_context,
            conversation_context=conversation_context,
        )

        fallback_used = False
        try:
            llm_response = self.provider.generate(prompt, system=SYSTEM_PROMPT)
            response_text = self.parser.parse(
                llm_response.content, llm_response.provider, llm_response.model
            ).content
        except LLMUnavailableError:
            fallback_used = True
            response_text = self.fallback.compose(message, twin_summary, gaps, memory_context)

        self.sessions.add_message(user_id, session_id, "user", message)
        self.sessions.add_message(user_id, session_id, "assistant", response_text)

        twin_updates = self._learn_from_message(user_id, message, known_skills=[
            skill["skill_name"] for skill in twin_repo.list_user_skills(user_id)
        ])
        return {
            "response": response_text,
            "session_id": session_id,
            "fallback": fallback_used,
            "twin_updates": twin_updates,
        }

    # ---------------------------------------------------------------- helpers
    def _resolve_session(self, user_id: str, session_id: str | None) -> dict:
        if session_id:
            session = self.sessions.get_session(user_id, session_id)
            if session:
                return session
        return self.sessions.create_session(user_id)

    def _render_twin_context(self, summary, gaps: list) -> str:
        lines = [
            f"Name: {summary.display_name or 'unknown'}",
            f"Career goal: {summary.primary_goal or 'not set'}",
            f"Target role: {summary.target_role or 'not set'} (rubric: {summary.role_key})",
            f"Skills tracked: {summary.skills_count}, average level: {summary.avg_level}/5",
            f"Open gaps: {summary.gaps_count}; top gaps: {', '.join(summary.top_gaps) or 'none'}",
            f"Projects: {summary.projects_count}",
            f"Readiness score: {summary.readiness_score}/100",
        ]
        for gap in gaps[:6]:
            lines.append(
                f"GAP {gap.skill_name}: {gap.current_level}->{gap.target_level} "
                f"({gap.priority}). {gap.reason}"
            )
        if summary.roadmap_progress:
            progress = summary.roadmap_progress
            lines.append(
                f"Roadmap '{progress.get('goal', '')}': "
                f"{progress.get('completed', 0)}/{progress.get('total', 0)} done."
            )
        for event in summary.recent_events[:5]:
            lines.append(f"Recent event {event['type']}: {event['data']} ({event['at']})")
        return "\n".join(lines)

    def _render_knowledge(self, message: str) -> str:
        results = self.knowledge.retrieve_many(message)
        if not results:
            return ""
        lines = []
        for result in results:
            lines.append(f"[{result.topic} | score {result.score}]")
            lines.extend(f"- {fact}" for fact in result.facts)
        return "\n".join(lines)

    def _render_conversation(self, user_id: str, session_id: str) -> str:
        messages = self.sessions.recent_messages(user_id, session_id, limit=10)
        if not messages:
            return ""
        return "\n".join(f"{m['role']}: {m['content'][:500]}" for m in messages)

    # ------------------------------------------------------- learning loop
    def _learn_from_message(self, user_id: str, message: str, known_skills: list) -> list:
        updates: list = []
        extracted = self._extract_facts(message, known_skills)
        for skill_name in extracted.mentioned_skills:
            change = twin_service.add_skill_evidence(
                user_id, skill_name, source="chat", note=f"Mentioned in chat: {message[:120]}"
            )
            updates.append({"type": "skill_evidence", "skill": skill_name,
                            "new_level": change["new_level"]})
        if extracted.goal_statement:
            twin_repo.update_profile(user_id, {"primary_goal": extracted.goal_statement})
            memory_repo.record_event(user_id, "career_goal_changed",
                                     data={"goal": extracted.goal_statement, "via": "chat"})
            self.memory.remember(user_id, "goal", f"Career goal: {extracted.goal_statement}",
                                 importance=9)
            updates.append({"type": "goal", "goal": extracted.goal_statement})
        if extracted.completed_activity:
            memory_repo.record_event(user_id, "activity_completed",
                                     data={"activity": extracted.completed_activity, "via": "chat"})
            self.memory.remember(user_id, "achievement", extracted.completed_activity,
                                 importance=7)
            updates.append({"type": "activity", "activity": extracted.completed_activity})
        if extracted.preference_statement:
            self.memory.remember(user_id, "preference", extracted.preference_statement,
                                 importance=6)
            updates.append({"type": "preference", "preference": extracted.preference_statement})
        return updates

    def _extract_facts(self, message: str, known_skills: list) -> ChatTwinUpdate:
        """LLM structured extraction when available, else deterministic heuristics."""
        if self.provider.configured:
            try:
                prompt = self.prompts.build_extraction_prompt(message, known_skills)
                llm_response = self.provider.generate(prompt, system=None,
                                                      max_output_tokens=256)
                return self.parser.parse_json(llm_response.content, ChatTwinUpdate)
            except Exception:
                pass  # fall through to heuristics
        return self._heuristic_extract(message)

    def _heuristic_extract(self, message: str) -> ChatTwinUpdate:
        mentioned = [s for s in self.extractor.extract(message)]

        def _first(patterns: list) -> str:
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return re.sub(r"\s+", " ", match.group(1)).strip()[:200]
            return ""

        goal = _first(_GOAL_PATTERNS)
        goal = re.sub(r"^to\s+", "", goal, flags=re.IGNORECASE).strip()
        return ChatTwinUpdate(
            mentioned_skills=mentioned,
            goal_statement=goal,
            completed_activity=_first(_DONE_PATTERNS),
            preference_statement=_first(_PREF_PATTERNS),
        )

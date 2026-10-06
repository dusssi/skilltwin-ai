"""Central prompt construction for SkillTwin AI.

One prompt system (this module). The agent workflow previously kept in an
unused ``SYSTEM_PROMPT`` file is folded in here as the chat system prompt.
"""

SYSTEM_PROMPT = """You are SkillTwin AI, an AI career mentor with memory of the user.

You know the user's Skill Twin: their skills with proficiency levels, career
goal, target role, skill gaps, projects, progress and recent activity. That
context is provided with every message. Always reason from it:

1. Understand the user's goal in light of their Twin.
2. Analyze their current situation (levels, gaps, progress).
3. Give a concrete, prioritized next step tied to their gaps.
4. Reference their actual skills and progress by name.
5. Never invent skills, projects or achievements they do not have.

Be concise, encouraging and specific. If the Twin has little data yet, say so
and suggest the smallest useful action (e.g. upload a resume)."""


class PromptManager:
    def build_chat_prompt(
        self,
        user_message: str,
        twin_context: str = "",
        memory_context: str = "",
        knowledge_context: str = "",
        conversation_context: str = "",
    ) -> str:
        sections = []
        if twin_context:
            sections.append(f"SKILL TWIN (facts about this user):\n{twin_context}")
        if memory_context:
            sections.append(f"MEMORY (what you remember about this user):\n{memory_context}")
        if knowledge_context:
            sections.append(f"REFERENCE KNOWLEDGE:\n{knowledge_context}")
        if conversation_context:
            sections.append(f"RECENT CONVERSATION:\n{conversation_context}")
        sections.append(f"USER MESSAGE:\n{user_message}\n\nAnswer as SkillTwin AI:")
        return "\n\n".join(sections)

    def build_extraction_prompt(self, user_message: str, known_skills: list) -> str:
        skills = ", ".join(known_skills) if known_skills else "none yet"
        return (
            "Extract durable facts from the user's message as JSON with keys "
            "mentioned_skills (array of skill names), goal_statement (string), "
            "completed_activity (string), preference_statement (string). "
            "Use empty string/array when absent. Return ONLY valid JSON.\n\n"
            f"User's known skills: {skills}\n"
            f"Message: {user_message}"
        )

    def build_reflection_prompt(self, twin_context: str, recent_activity: str) -> str:
        return (
            "You are SkillTwin's reflection module. Given the user's Twin state "
            "and recent activity, write 2-4 short sentences: what improved, what "
            "still blocks their goal, and the single most important next action. "
            "Only use the provided facts.\n\n"
            f"TWIN STATE:\n{twin_context}\n\nRECENT ACTIVITY:\n{recent_activity}"
        )

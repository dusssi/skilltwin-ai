"""Canonical SkillTwin orchestrator (the ONE agent execution architecture).

Pipeline::

    observe → plan → act (specialists) → reflect → finish

* Observe loads the real Twin summary, gaps, roadmap progress and memory.
* Plan builds typed steps from actual state (no static script).
* Act runs skill/roadmap/recommendation/research specialists and persists
  every artifact (gaps, roadmap, recommendations, research).
* Reflect scores progress from real deltas and records an agent-run event.

All inter-agent communication uses typed Pydantic state (``AgentRunState``).
"""

from app.agents.specialist.registry import AgentRegistry
from app.agents.state import AgentRunState
from app.db import memory as memory_repo
from app.db import twin as twin_repo
from app.memory.memory_manager import MemoryManager
from app.planner.planner import Planner
from app.reflection.models import ReflectionInput
from app.twin import service as twin_service


class OrchestratorAgent:
    """Single entry point for autonomous Twin maintenance runs."""

    def __init__(self):
        self.planner = Planner()
        self.registry = AgentRegistry()
        self.memory = MemoryManager()

    # ------------------------------------------------------------------ run
    def run(self, user_id: str, goal: str | None = None) -> AgentRunState:
        state = AgentRunState(user_id=user_id, status="running")
        if goal:
            twin_repo.update_profile(user_id, {"primary_goal": goal})
            state.goal = goal

        state = self.observe(state)
        state = self.plan(state)
        state = self.act(state)
        state = self.reflect(state)
        state = self.finish(state)
        return state

    # ---------------------------------------------------------------- phases
    def observe(self, state: AgentRunState) -> AgentRunState:
        summary = twin_service.build_summary(state.user_id)
        if not state.goal:
            state.goal = summary.primary_goal or summary.target_role or "Career growth"
        state.observations = [
            f"Goal: {state.goal}",
            f"Target role: {summary.target_role or 'not set'} (rubric: {summary.role_key})",
            f"Skills: {summary.skills_count} tracked, avg level {summary.avg_level}/5",
            f"Gaps: {summary.gaps_count} open; top: {', '.join(summary.top_gaps) or 'none'}",
            f"Projects: {summary.projects_count}",
        ]
        if summary.roadmap_progress:
            progress = summary.roadmap_progress
            state.observations.append(
                f"Roadmap: {progress.get('completed', 0)}/{progress.get('total', 0)} done"
            )
        else:
            state.observations.append("Roadmap: none yet")
        state.observations.append(f"Readiness: {summary.readiness_score}/100")
        memories = self.memory.recall(state.user_id, limit=5)
        for memory in memories:
            state.observations.append(f"Memory [{memory['kind']}]: {memory['content']}")
        return state

    def plan(self, state: AgentRunState) -> AgentRunState:
        summary = twin_service.build_summary(state.user_id)
        progress = summary.roadmap_progress or {}
        state.plan = self.planner.create_plan(state.goal, {
            "gaps_open": summary.gaps_count,
            "roadmap_total": progress.get("total", 0),
            "skills_count": summary.skills_count,
        })
        return state

    def act(self, state: AgentRunState) -> AgentRunState:
        user_id = state.user_id
        for step in state.plan.steps:
            if step.name in {"observe", "reflect"}:
                state.completed_steps.append(step.name)
                continue
            if step.name in {"analyze_gaps", "bootstrap_twin"}:
                agent = self.registry.get_agent("skill_agent")
                state.gaps = agent.run(user_id)["gaps"]
            elif step.name == "generate_roadmap":
                agent = self.registry.get_agent("roadmap_agent")
                state.roadmap = agent.run(user_id, goal=state.goal)
            elif step.name == "recommend":
                agent = self.registry.get_agent("recommendation_agent")
                state.recommendations = agent.run(user_id)
            elif step.name == "research":
                agent = self.registry.get_agent("research_agent")
                result = agent.research(state.goal or "career growth")
                state.research = result.model_dump()
            state.completed_steps.append(step.name)
        # Ensure roadmap context exists for reflection even when generation
        # was skipped (active roadmap already present).
        if not state.roadmap:
            agent = self.registry.get_agent("roadmap_agent")
            state.roadmap = agent.run(user_id, goal=state.goal)
        return state

    def reflect(self, state: AgentRunState) -> AgentRunState:
        summary = twin_service.build_summary(state.user_id)
        progress = summary.roadmap_progress or {}
        history = twin_repo.list_skill_history(state.user_id, limit=10)
        improved = sorted({entry["skill_name"] for entry in history})
        events = memory_repo.list_events(state.user_id, limit=10)
        reflector = self.registry.get_agent("reflection_agent")
        result = reflector.reflect(ReflectionInput(
            goal=state.goal,
            gaps_closed=max(0, summary.skills_count - summary.gaps_count),
            gaps_open=summary.gaps_count,
            roadmap_completed=progress.get("completed", 0),
            roadmap_total=progress.get("total", 0),
            skills_improved=improved,
            recent_events=[event["event_type"] for event in events],
        ))
        state.reflection = result.model_dump()
        return state

    def finish(self, state: AgentRunState) -> AgentRunState:
        reflection = state.reflection or {}
        state.summary = (
            f"Agent run for goal '{state.goal}': {len(state.completed_steps)} steps, "
            f"{len(state.gaps)} open gaps, reflection score "
            f"{reflection.get('score', 0)}/10."
        )
        state.status = "completed"
        memory_repo.record_event(
            state.user_id, "agent_run_completed",
            data={"goal": state.goal, "steps": state.completed_steps,
                  "open_gaps": len(state.gaps),
                  "reflection_score": reflection.get("score", 0)},
        )
        return state

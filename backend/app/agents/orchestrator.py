from app.state.state import AgentState
from app.planner.planner import Planner

from app.memory.models import (
    MemoryRecord
)

from app.memory.memory_manager import (
    MemoryManager
)

from app.agents.specialist.registry import (
    AgentRegistry
)

from app.sessions.session_manager import (
    SessionManager
)

from app.context.engine import (
    ContextEngine
)

from app.reflection.reflector import (
    Reflector
)

from app.research.research_agent import (
    ResearchAgent
)


class OrchestratorAgent:

    def __init__(self):

        self.planner = Planner()

        self.memory_manager = (
            MemoryManager()
        )

        self.agent_registry = (
            AgentRegistry()
        )

        self.session_manager = (
            SessionManager()
        )

        self.context_engine = (
            ContextEngine()
        )

        self.research_agent = (
            ResearchAgent()
        )

        self.reflector = (
            Reflector()
        )

    def run(
        self,
        user_id: str,
        session_id: str,
        goal: str
    ) -> AgentState:

        # Create / Load Session

        session = self.session_manager.get_session(
            session_id
        )

        if session is None:

            session = (
                self.session_manager.create_session(
                    session_id,
                    user_id
                )
            )

        # Store User Message

        self.session_manager.add_message(
            session_id,
            goal
        )

        # Retrieve Context

        context = self.context_engine.get_context(
            goal,
            session.messages
        )

        # Load Existing Memory

        memory = self.memory_manager.load_memory(
            user_id
        )

        if memory and not goal:

            goal = memory.goal

        # Research Phase

        research = self.research_agent.research(
            goal
        )

        # Create Runtime State

        state = AgentState(
            user_goal=goal
        )

        # Store Context

        if context:

            state.observations.append(
                f"Relevant Context: {context}"
            )

        # Store Research Result

        state.research_result = {

            "query": research.query,

            "evidence": research.evidence,

            "conclusion": research.conclusion
        }

        # Create Plan

        state = self.planner.create_plan(
            state
        )

        # Specialist Agents

        skill_agent = self.agent_registry.get_agent(
            "skill_agent"
        )

        roadmap_agent = self.agent_registry.get_agent(
            "roadmap_agent"
        )

        project_agent = self.agent_registry.get_agent(
            "project_agent"
        )

        # Execute Agents

        skills = skill_agent.run(
            state.user_goal
        )

        roadmap = roadmap_agent.run(
            state.user_goal
        )

        projects = project_agent.run(
            state.user_goal
        )

        # Store Tool Results

        state.tool_results = {

            "skills": skills,

            "roadmap": roadmap,

            "projects": projects
        }

        # Reflection Phase

        reflection = self.reflector.reflect(
            skills
        )

        state.reflection_result = {

            "issues": reflection.issues,

            "suggestions": reflection.suggestions,

            "score": reflection.score
        }

        # Save Memory

        memory_record = MemoryRecord(
            user_id=user_id,
            goal=state.user_goal,
            completed_tasks=state.completed_tasks,
            observations=state.observations
        )

        self.memory_manager.save_memory(
            memory_record
        )

        # Final Response

        state.final_response = (
            f"Goal: {state.user_goal}\n\n"

            f"Context:\n"
            f"{context}\n\n"

            f"Research Evidence:\n"
            f"{research.evidence}\n\n"

            f"Research Conclusion:\n"
            f"{research.conclusion}\n\n"

            f"Skills:\n"
            f"{skills}\n\n"

            f"Roadmap:\n"
            f"{roadmap}\n\n"

            f"Projects:\n"
            f"{projects}\n\n"

            f"Reflection Score:\n"
            f"{reflection.score}/10\n\n"

            f"Issues:\n"
            f"{reflection.issues}\n\n"

            f"Suggestions:\n"
            f"{reflection.suggestions}"
        )

        # Store Assistant Response

        self.session_manager.add_message(
            session_id,
            state.final_response
        )

        return state
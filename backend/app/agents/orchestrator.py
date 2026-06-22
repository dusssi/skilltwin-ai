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


class OrchestratorAgent:

    def __init__(self):

        self.planner = Planner()

        self.memory_manager = (
            MemoryManager()
        )

        self.agent_registry = (
            AgentRegistry()
        )

    def run(
        self,
        user_id: str,
        goal: str
    ) -> AgentState:

        # Load Existing Memory
        memory = self.memory_manager.load_memory(
            user_id
        )

        if memory:

            goal = memory.goal

        # Create Runtime State
        state = AgentState(
            user_goal=goal
        )

        # Create Plan
        state = self.planner.create_plan(
            state
        )

        # Delegate To Specialist Agents

        skill_agent = self.agent_registry.get_agent(
            "skill_agent"
        )

        roadmap_agent = self.agent_registry.get_agent(
            "roadmap_agent"
        )

        project_agent = self.agent_registry.get_agent(
            "project_agent"
        )

        skills = skill_agent.run(
            state.user_goal
        )

        roadmap = roadmap_agent.run(
            state.user_goal
        )

        projects = project_agent.run(
            state.user_goal
        )

        # Store Results

        state.tool_results = {

            "skills": skills,

            "roadmap": roadmap,

            "projects": projects
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
            f"Skills:\n{skills}\n\n"
            f"Roadmap:\n{roadmap}\n\n"
            f"Projects:\n{projects}"
        )

        return state
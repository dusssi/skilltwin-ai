from app.state.state import AgentState
from app.planner.planner import Planner

from app.memory.models import (
    MemoryRecord
)

from app.memory.memory_manager import (
    MemoryManager
)

from app.tools.registry import (
    ToolRegistry
)


class OrchestratorAgent:

    def __init__(self):

        self.planner = Planner()

        self.memory_manager = (
            MemoryManager()
        )

        self.registry = (
            ToolRegistry()
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

        # Execute Tools

        skill_tool = self.registry.get_tool(
            "skill_tool"
        )

        roadmap_tool = self.registry.get_tool(
            "roadmap_tool"
        )

        project_tool = self.registry.get_tool(
            "project_tool"
        )

        skills = skill_tool.execute(
            state.user_goal
        )

        roadmap = roadmap_tool.execute(
            state.user_goal
        )

        projects = project_tool.execute(
            state.user_goal
        )

        # Store Tool Results
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

        # Generate Response
        state.final_response = (
            f"Goal: {state.user_goal}\n\n"
            f"Skills:\n{skills}\n\n"
            f"Projects:\n{projects}"
        )

        return state
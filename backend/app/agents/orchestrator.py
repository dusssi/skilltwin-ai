from app.state.state import AgentState
from app.planner.planner import Planner

from app.memory.models import (
    MemoryRecord
)

from app.memory.memory_manager import (
    MemoryManager
)


class OrchestratorAgent:

    def __init__(self):

        self.planner = Planner()

        self.memory_manager = (
            MemoryManager()
        )

    def run(
        self,
        goal: str
    ) -> AgentState:

        # Load Memory
        memory = self.memory_manager.load_memory(
            "dushyant"
        )

        if memory:

            goal = memory.goal

        # Create State
        state = AgentState(
            user_goal=goal
        )

        # Generate Plan
        state = self.planner.create_plan(
            state
        )

        # Save Memory
        memory_record = MemoryRecord(
            user_id="dushyant",
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
            f"Plan Generated Successfully"
        )

        return state
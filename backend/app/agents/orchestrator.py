from app.state.state import AgentState
from app.planner.planner import Planner


class OrchestratorAgent:

    def __init__(self):

        self.planner = Planner()

    def run(
        self,
        goal: str
    ) -> AgentState:

        # Create State
        state = AgentState(
            user_goal=goal
        )

        # Generate Plan
        state = self.planner.create_plan(
            state
        )

        # Generate Response
        state.final_response = (
            f"Goal: {goal}\n\n"
            f"Plan Generated Successfully"
        )

        return state
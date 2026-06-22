from app.state.state import AgentState
from app.planner.planner import Planner


state = AgentState(
    user_goal="Get AI Internship"
)

planner = Planner()

updated_state = planner.create_plan(
    state
)

print(updated_state.current_plan)
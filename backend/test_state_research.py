from app.state.state import (
    AgentState
)

state = AgentState(
    user_goal="AI Internship"
)

state.research_result = {

    "evidence": [
        "Python required",
        "Git required"
    ],

    "conclusion":
    "Learn Python and Git"
}

print(state)
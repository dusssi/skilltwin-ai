from app.state.state import (
    AgentState
)

state = AgentState(
    user_goal="AI Internship"
)

state.reflection_result = {

    "issues": [
        "Git missing"
    ],

    "suggestions": [
        "Learn Git"
    ],

    "score": 7
}

print(state)
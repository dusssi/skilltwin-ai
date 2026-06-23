# test_profile_runtime.py

from app.agents.orchestrator import (
    OrchestratorAgent
)

agent = OrchestratorAgent()

state = agent.run(

    user_id="user123",

    session_id="session1",

    goal="AI Internship"
)

print("\nREFLECTION:\n")

print(
    state.reflection_result
)

print("\nPROFILE SAVED")
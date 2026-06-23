from app.agents.orchestrator import (
    OrchestratorAgent
)

agent = OrchestratorAgent()

result = agent.run(
    user_id="dushyant",
    session_id="session_001",
    goal="FastAPI"
)

print("\nREFLECTION RESULT:\n")

print(
    result.reflection_result
)

print("\nFINAL RESPONSE:\n")

print(
    result.final_response
)
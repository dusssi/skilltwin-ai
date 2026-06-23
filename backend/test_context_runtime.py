from app.agents.orchestrator import (
    OrchestratorAgent
)

agent = OrchestratorAgent()

result = agent.run(
    user_id="dushyant",
    session_id="session_001",
    goal="FastAPI"
)

print("\nOBSERVATIONS:\n")

print(
    result.observations
)

print("\nFINAL RESPONSE:\n")

print(
    result.final_response
)
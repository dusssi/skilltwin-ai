from app.agents.orchestrator import (
    OrchestratorAgent
)

agent = OrchestratorAgent()

result = agent.run(
    user_id="dushyant",
    session_id="session_001",
    goal="AI Internship"
)

print("\nTOOL RESULTS:\n")

print(
    result.tool_results
)

print("\nFINAL RESPONSE:\n")

print(
    result.final_response
)
from app.agents.orchestrator import (
    OrchestratorAgent
)

agent = OrchestratorAgent()

result = agent.run(
    user_id="dushyant",
    goal="AI Engineer"
)

print(result.tool_results)

print("\n")

print(result.final_response)
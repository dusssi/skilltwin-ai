from app.agents.orchestrator import OrchestratorAgent


agent = OrchestratorAgent()

result = agent.run(
    "Get AI Internship"
)

print(result)
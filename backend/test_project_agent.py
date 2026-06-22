from app.agents.specialist.project_agent import (
    ProjectAgent
)

agent = ProjectAgent()

result = agent.run(
    "AI Engineer"
)

print(result)
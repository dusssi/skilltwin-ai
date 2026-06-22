from app.agents.specialist.registry import (
    AgentRegistry
)

registry = AgentRegistry()

agent = registry.get_agent(
    "skill_agent"
)

result = agent.run(
    "AI Engineer"
)

print(result)
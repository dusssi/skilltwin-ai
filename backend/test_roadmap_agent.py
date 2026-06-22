from app.agents.specialist.roadmap_agent import (
    RoadmapAgent
)

agent = RoadmapAgent()

result = agent.run(
    "AI Engineer"
)

print(result)
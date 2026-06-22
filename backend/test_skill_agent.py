from app.agents.specialist.skill_agent import (
    SkillAgent
)

agent = SkillAgent()

result = agent.run(
    "AI Engineer"
)

print(result)
from app.agents.orchestrator import (
    OrchestratorAgent
)

agent = OrchestratorAgent()

user1 = agent.run(
    user_id="dushyant",
    goal="AI Internship"
)

user2 = agent.run(
    user_id="rahul",
    goal="Data Scientist"
)

print(user1.user_goal)
print(user2.user_goal)
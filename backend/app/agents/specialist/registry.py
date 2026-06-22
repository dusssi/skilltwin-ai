from app.agents.specialist.skill_agent import (
    SkillAgent
)

from app.agents.specialist.roadmap_agent import (
    RoadmapAgent
)

from app.agents.specialist.project_agent import (
    ProjectAgent
)


class AgentRegistry:

    def __init__(self):

        self.agents = {

            "skill_agent":
                SkillAgent(),

            "roadmap_agent":
                RoadmapAgent(),

            "project_agent":
                ProjectAgent()
        }

    def get_agent(
        self,
        agent_name: str
    ):

        return self.agents.get(
            agent_name
        )
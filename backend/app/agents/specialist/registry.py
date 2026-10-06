"""Registry of live specialist agents."""

from app.agents.specialist.recommendation_agent import RecommendationAgent
from app.agents.specialist.resume_agent import ResumeAgent
from app.agents.specialist.roadmap_agent import RoadmapAgent
from app.agents.specialist.skill_agent import SkillAgent
from app.reflection.reflector import Reflector
from app.research.research_agent import ResearchAgent


class AgentRegistry:
    def __init__(self):
        self.agents = {
            "skill_agent": SkillAgent(),
            "roadmap_agent": RoadmapAgent(),
            "resume_agent": ResumeAgent(),
            "recommendation_agent": RecommendationAgent(),
            "research_agent": ResearchAgent(),
            "reflection_agent": Reflector(),
        }

    def get_agent(self, agent_name: str):
        return self.agents.get(agent_name)

    def names(self) -> list:
        return sorted(self.agents.keys())

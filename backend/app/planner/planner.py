"""Typed planner: goal + Twin state → ordered plan steps."""

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    name: str
    detail: str = ""
    agent: str = "orchestrator"


class Plan(BaseModel):
    goal: str = ""
    steps: list[PlanStep] = Field(default_factory=list)


class Planner:
    def create_plan(self, goal: str, twin_state: dict) -> Plan:
        goal_text = (goal or "").strip()
        gaps_open = int(twin_state.get("gaps_open", 0))
        roadmap_total = int(twin_state.get("roadmap_total", 0))
        skills_count = int(twin_state.get("skills_count", 0))

        steps: list[PlanStep] = [PlanStep(name="observe", detail="Load Twin, memory and progress.")]
        if skills_count == 0:
            steps.append(PlanStep(name="bootstrap_twin",
                                  detail="No skills yet: request resume or record stated skills.",
                                  agent="skill_agent"))
        if gaps_open:
            steps.append(PlanStep(name="analyze_gaps",
                                  detail=f"Compute and snapshot {gaps_open} open gaps.",
                                  agent="skill_agent"))
        if roadmap_total == 0 and (gaps_open or skills_count):
            steps.append(PlanStep(name="generate_roadmap",
                                  detail="Build a personalized roadmap from gaps.",
                                  agent="roadmap_agent"))
        steps.append(PlanStep(name="recommend",
                              detail="Refresh project/internship/action recommendations.",
                              agent="recommendation_agent"))
        steps.append(PlanStep(name="research",
                              detail=f"Gather reference knowledge for: {goal_text or 'career growth'}.",
                              agent="research_agent"))
        steps.append(PlanStep(name="reflect",
                              detail="Score progress and derive next actions.",
                              agent="reflection_agent"))
        return Plan(goal=goal_text, steps=steps)

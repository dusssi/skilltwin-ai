from app.tools.registry import (
    ToolRegistry
)


class SkillAgent:

    def __init__(self):

        self.registry = ToolRegistry()

    def run(
        self,
        goal: str
    ):

        skill_tool = self.registry.get_tool(
            "skill_tool"
        )

        result = skill_tool.execute(
            goal
        )

        return result
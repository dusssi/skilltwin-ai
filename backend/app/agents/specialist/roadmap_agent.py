from app.tools.registry import (
    ToolRegistry
)


class RoadmapAgent:

    def __init__(self):

        self.registry = ToolRegistry()

    def run(
        self,
        goal: str
    ):

        roadmap_tool = self.registry.get_tool(
            "roadmap_tool"
        )

        result = roadmap_tool.execute(
            goal
        )

        return result
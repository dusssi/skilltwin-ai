from app.tools.registry import (
    ToolRegistry
)


class ProjectAgent:

    def __init__(self):

        self.registry = ToolRegistry()

    def run(
        self,
        goal: str
    ):

        project_tool = self.registry.get_tool(
            "project_tool"
        )

        result = project_tool.execute(
            goal
        )

        return result
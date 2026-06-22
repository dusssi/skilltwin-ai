from app.tools.skill_tool import (
    SkillTool
)

from app.tools.roadmap_tool import (
    RoadmapTool
)

from app.tools.project_tool import (
    ProjectTool
)


class ToolRegistry:

    def __init__(self):

        self.tools = {

            "skill_tool":
                SkillTool(),

            "roadmap_tool":
                RoadmapTool(),

            "project_tool":
                ProjectTool()
        }

    def get_tool(
        self,
        tool_name: str
    ):

        return self.tools.get(
            tool_name
        )
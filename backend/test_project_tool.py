from app.tools.project_tool import (
    ProjectTool
)

tool = ProjectTool()

projects = tool.execute(
    "AI Engineer"
)

print(projects)
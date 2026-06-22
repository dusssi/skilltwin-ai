from app.tools.roadmap_tool import (
    RoadmapTool
)

tool = RoadmapTool()

roadmap = tool.execute(
    "AI Engineer"
)

print(roadmap)
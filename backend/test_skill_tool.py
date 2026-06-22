from app.tools.skill_tool import (
    SkillTool
)

tool = SkillTool()

skills = tool.execute(
    "AI Engineer"
)

print(skills)
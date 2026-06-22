from app.tools.registry import (
    ToolRegistry
)

registry = ToolRegistry()

tool = registry.get_tool(
    "skill_tool"
)

result = tool.execute(
    "AI Engineer"
)

print(result)
from app.tools.base_tool import (
    BaseTool
)


class SkillTool(BaseTool):

    @property
    def name(self):

        return "skill_tool"

    def execute(
        self,
        input_data: str
    ):

        role = input_data.lower()

        if "ai" in role:

            return [
                "Python",
                "DSA",
                "FastAPI",
                "SQL",
                "Docker"
            ]

        elif "data" in role:

            return [
                "Python",
                "Pandas",
                "NumPy",
                "SQL",
                "Machine Learning"
            ]

        return [
            "Communication",
            "Problem Solving"
        ]
from app.tools.base_tool import (
    BaseTool
)


class RoadmapTool(BaseTool):

    @property
    def name(self):

        return "roadmap_tool"

    def execute(
        self,
        input_data: str
    ):

        role = input_data.lower()

        if "ai" in role:

            return {
                "Month 1": [
                    "Python",
                    "DSA"
                ],
                "Month 2": [
                    "FastAPI",
                    "SQL"
                ],
                "Month 3": [
                    "Docker",
                    "Projects"
                ]
            }

        return {
            "Month 1": [
                "Communication",
                "Problem Solving"
            ]
        }
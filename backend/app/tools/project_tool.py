from app.tools.base_tool import (
    BaseTool
)


class ProjectTool(BaseTool):

    @property
    def name(self):

        return "project_tool"

    def execute(
        self,
        input_data: str
    ):

        role = input_data.lower()

        if "ai" in role:

            return [
                "SkillTwin AI",
                "AI Interview Analytics",
                "Career Copilot"
            ]

        elif "data" in role:

            return [
                "Sales Forecasting",
                "Customer Churn Prediction",
                "Recommendation System"
            ]

        return [
            "Portfolio Website"
        ]
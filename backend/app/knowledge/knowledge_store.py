from app.knowledge.models import (
    KnowledgeItem
)


class KnowledgeStore:

    def __init__(self):

        self.items = [

            KnowledgeItem(
                topic="AI Internship",
                facts=[
                    "Python required",
                    "Git required",
                    "Portfolio required"
                ]
            ),

            KnowledgeItem(
                topic="FastAPI",
                facts=[
                    "Learn Routing",
                    "Learn Dependency Injection",
                    "Build APIs"
                ]
            ),

            KnowledgeItem(
                topic="Docker",
                facts=[
                    "Containerization",
                    "Dockerfile",
                    "Docker Compose"
                ]
            )
        ]

    def get_all_items(
        self
    ):

        return self.items
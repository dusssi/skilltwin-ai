from app.knowledge.models import (
    KnowledgeItem
)

item = KnowledgeItem(
    topic="AI Internship",
    facts=[
        "Python required",
        "Git required",
        "Portfolio required"
    ]
)

print(item)
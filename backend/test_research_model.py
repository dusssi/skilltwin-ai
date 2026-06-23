from app.research.models import (
    ResearchResult
)

result = ResearchResult(
    query="AI Internship",
    evidence=[
        "Python required",
        "Git required"
    ],
    conclusion=(
        "Learn Python and Git first."
    )
)

print(result)
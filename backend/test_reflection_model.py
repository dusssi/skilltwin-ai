from app.reflection.models import (
    ReflectionResult
)

result = ReflectionResult(
    issues=[
        "Git missing"
    ],
    suggestions=[
        "Learn Git"
    ],
    score=7
)

print(result)
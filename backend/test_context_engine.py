from app.context.engine import (
    ContextEngine
)

messages = [

    "Learn Python",

    "Learn FastAPI",

    "Build Advanced FastAPI Project",

    "Apply Internship"
]

engine = ContextEngine()

context = engine.get_context(
    "FastAPI",
    messages
)

print(context)
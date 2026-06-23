from app.context.retriever import (
    ContextRetriever
)

messages = [

    "Learn Python",

    "Learn FastAPI",

    "Build Portfolio",

    "Apply Internship"
]

retriever = ContextRetriever()

results = retriever.retrieve(
    "FastAPI",
    messages
)

print(results)
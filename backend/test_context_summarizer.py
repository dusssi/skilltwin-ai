from app.context.summarizer import (
    ContextSummarizer
)

results = [

    "Build Advanced FastAPI Project",

    "Learn FastAPI",

    "FastAPI"
]

summarizer = ContextSummarizer()

summary = summarizer.summarize(
    results
)

print(summary)
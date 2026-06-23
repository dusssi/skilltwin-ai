from app.context.ranking import (
    ContextRanker
)

results = [

    "FastAPI",

    "Learn FastAPI",

    "Build Advanced FastAPI Project"
]

ranker = ContextRanker()

ranked = ranker.rank(
    results
)

print(ranked)
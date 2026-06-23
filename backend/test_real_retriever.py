from app.knowledge.retriever import (
    KnowledgeRetriever
)

retriever = (
    KnowledgeRetriever()
)

result = retriever.retrieve(
    "AI Engineer Career"
)

print(result)
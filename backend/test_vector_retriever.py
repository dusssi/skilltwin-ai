from app.knowledge.retriever import (
    KnowledgeRetriever
)

retriever = KnowledgeRetriever()

facts = retriever.retrieve(
    "AI Engineer Career"
)

print(facts)
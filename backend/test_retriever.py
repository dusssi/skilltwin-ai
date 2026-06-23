from app.knowledge.retriever import (
    KnowledgeRetriever
)

retriever = KnowledgeRetriever()

facts = retriever.retrieve(
    "AI Internship"
)

print(facts)
from app.rag.rag_engine import (
    RAGEngine
)

engine = RAGEngine()

result = engine.generate(
    "How do I get an AI Internship?"
)

print("\nRETRIEVAL:\n")

print(
    result["retrieval"]
)

print("\nCONTEXT:\n")

print(
    result["context"]
)

print("\nMODEL:\n")

print(
    result["model"]
)

print("\nPROVIDER:\n")

print(
    result["provider"]
)

print("\nRESPONSE:\n")

print(
    result["response"]
)
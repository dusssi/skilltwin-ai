from app.rag.rag_engine import (
    RAGEngine
)

engine = RAGEngine()

result = engine.generate(
    "AI Engineer Career"
)

print("\nRETRIEVAL:\n")
print(result["retrieval"])

print("\nCONTEXT:\n")
print(result["context"])

print("\nPROMPT:\n")
print(result["prompt"])

print("\nRESPONSE:\n")
print(result["response"])
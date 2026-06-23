from app.vector.embedding import (
    EmbeddingEngine
)

engine = EmbeddingEngine()

vector = engine.embed(
    "AI Internship"
)

print(vector)
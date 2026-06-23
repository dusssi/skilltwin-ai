from app.embeddings.encoder import (
    TextEncoder
)

encoder = TextEncoder()

vector = encoder.encode(
    "AI Internship"
)

print(
    f"Dimensions: {len(vector)}"
)

print(
    vector[:10]
)
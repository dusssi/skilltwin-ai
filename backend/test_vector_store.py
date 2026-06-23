from app.vector.vector_store import (
    VectorStore
)

store = VectorStore()

print(
    store.get_vectors()
)
from app.vector.embedding import (
    EmbeddingEngine
)

from app.knowledge.knowledge_store import (
    KnowledgeStore
)


class VectorStore:

    def __init__(self):

        self.embedding_engine = (
            EmbeddingEngine()
        )

        self.knowledge_store = (
            KnowledgeStore()
        )

        self.vectors = {}

        self.build_store()

    def build_store(
        self
    ):

        items = (
            self.knowledge_store.get_all_items()
        )

        for item in items:

            self.vectors[
                item.topic
            ] = self.embedding_engine.embed(
                item.topic
            )

    def get_vectors(
        self
    ):

        return self.vectors
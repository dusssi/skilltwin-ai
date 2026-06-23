from app.vector.embedding import (
    EmbeddingEngine
)

from app.vector.vector_store import (
    VectorStore
)

from app.vector.similarity import (
    SimilarityEngine
)

from app.knowledge.knowledge_store import (
    KnowledgeStore
)


class KnowledgeRetriever:

    def __init__(self):

        self.embedding_engine = (
            EmbeddingEngine()
        )

        self.vector_store = (
            VectorStore()
        )

        self.similarity_engine = (
            SimilarityEngine()
        )

        self.knowledge_store = (
            KnowledgeStore()
        )

    def retrieve(
        self,
        query: str
    ):

        query_vector = (
            self.embedding_engine.embed(
                query
            )
        )

        vectors = (
            self.vector_store.get_vectors()
        )

        best_topic = None

        best_score = -1

        for topic, vector in vectors.items():

            score = (
                self.similarity_engine.calculate(
                    query_vector,
                    vector
                )
            )

            if score > best_score:

                best_score = score

                best_topic = topic

        for item in (
            self.knowledge_store.get_all_items()
        ):

            if item.topic == best_topic:

                return {
                    "topic": item.topic,
                    "score": round(
                        best_score,
                        4
                    ),
                    "facts": item.facts
                }

        return None
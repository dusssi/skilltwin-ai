from sentence_transformers import (
    SentenceTransformer
)

_model = None


class EmbeddingModel:

    def get_model(
        self
    ):

        global _model

        if _model is None:

            _model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return _model
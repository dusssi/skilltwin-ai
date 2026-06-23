from app.embeddings.model import (
    EmbeddingModel
)


class TextEncoder:

    def __init__(self):

        self.model = (
            EmbeddingModel()
            .get_model()
        )

    def encode(
        self,
        text: str
    ):

        vector = self.model.encode(
            text
        )

        return vector.tolist()
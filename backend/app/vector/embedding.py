from app.embeddings.encoder import (
    TextEncoder
)


class EmbeddingEngine:

    def __init__(self):

        self.encoder = (
            TextEncoder()
        )

    def embed(
        self,
        text: str
    ):

        return self.encoder.encode(
            text
        )
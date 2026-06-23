class EmbeddingEngine:

    def embed(
        self,
        text: str
    ):

        text = text.lower()

        keywords = [

            "ai",
            "internship",
            "engineer",
            "career",
            "fastapi",
            "docker"
        ]

        vector = []

        for keyword in keywords:

            if keyword in text:

                vector.append(1)

            else:

                vector.append(0)

        return vector
class SimilarityEngine:

    def calculate(
        self,
        vector_a: list,
        vector_b: list
    ):

        score = 0

        for a, b in zip(
            vector_a,
            vector_b
        ):

            score += abs(
                a - b
            )

        similarity = (
            1 / (1 + score)
        )

        return similarity
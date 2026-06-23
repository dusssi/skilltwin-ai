import numpy as np


class SimilarityEngine:

    def calculate(
        self,
        vector_a: list,
        vector_b: list
    ):

        a = np.array(
            vector_a
        )

        b = np.array(
            vector_b
        )

        numerator = np.dot(
            a,
            b
        )

        denominator = (
            np.linalg.norm(a)
            *
            np.linalg.norm(b)
        )

        if denominator == 0:

            return 0.0

        similarity = (
            numerator /
            denominator
        )

        return float(
            similarity
        )
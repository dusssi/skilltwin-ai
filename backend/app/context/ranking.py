class ContextRanker:

    def rank(
        self,
        results: list
    ):

        ranked = sorted(
            results,
            key=len,
            reverse=True
        )

        return ranked
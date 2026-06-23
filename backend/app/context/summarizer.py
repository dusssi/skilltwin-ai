class ContextSummarizer:

    def summarize(
        self,
        ranked_results: list
    ):

        if not ranked_results:

            return ""

        summary = " | ".join(
            ranked_results
        )

        return summary
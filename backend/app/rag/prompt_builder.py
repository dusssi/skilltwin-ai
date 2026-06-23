class PromptBuilder:

    def build(
        self,
        query: str,
        context: str
    ):

        prompt = (

            f"Question:\n"
            f"{query}\n\n"

            f"Context:\n"
            f"{context}\n\n"

            f"Answer:"
        )

        return prompt
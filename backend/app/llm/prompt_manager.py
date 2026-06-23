class PromptManager:

    def build_prompt(
        self,
        query: str,
        context: str
    ):

        system_prompt = (

            "You are SkillTwin AI, "
            "an AI career mentor."
        )

        prompt = (

            f"{system_prompt}\n\n"

            f"Context:\n"
            f"{context}\n\n"

            f"User Question:\n"
            f"{query}\n\n"

            f"Answer:"
        )

        return prompt
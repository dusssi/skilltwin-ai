from app.knowledge.retriever import (
    KnowledgeRetriever
)

from app.rag.context_builder import (
    ContextBuilder
)

from app.rag.prompt_builder import (
    PromptBuilder
)


class RAGEngine:

    def __init__(self):

        self.retriever = (
            KnowledgeRetriever()
        )

        self.context_builder = (
            ContextBuilder()
        )

        self.prompt_builder = (
            PromptBuilder()
        )

    def generate(
        self,
        query: str
    ):

        # Retrieve Knowledge

        retrieval = (
            self.retriever.retrieve(
                query
            )
        )

        # Handle No Results

        if not retrieval:

            return {

                "retrieval": None,

                "context": "",

                "prompt": "",

                "response": (
                    "No relevant knowledge "
                    "was found."
                )
            }

        # Build Context

        context = (
            self.context_builder.build(
                retrieval["facts"]
            )
        )

        # Build Prompt

        prompt = (
            self.prompt_builder.build(
                query,
                context
            )
        )

        # Extract Facts Safely

        facts = retrieval.get(
            "facts",
            []
        )

        # Generate Response

        response = (

            f"To achieve your goal of "
            f"'{query}', you should focus "
            f"on the following:\n\n"

            f"1. {facts[0] if len(facts) > 0 else 'Learn core fundamentals'}\n"

            f"2. {facts[1] if len(facts) > 1 else 'Build practical projects'}\n"

            f"3. {facts[2] if len(facts) > 2 else 'Create a strong portfolio'}\n\n"

            f"Similarity Score: "
            f"{retrieval['score']}\n\n"

            f"These recommendations were "
            f"generated using SkillTwin's "
            f"semantic retrieval and "
            f"knowledge base."
        )

        return {

            "retrieval": retrieval,

            "context": context,

            "prompt": prompt,

            "response": response
        }
from app.knowledge.retriever import (
    KnowledgeRetriever
)

from app.rag.context_builder import (
    ContextBuilder
)

from app.rag.prompt_builder import (
    PromptBuilder
)

from app.llm.provider import (
    LLMProvider
)

from app.llm.prompt_manager import (
    PromptManager
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

        self.prompt_manager = (
            PromptManager()
        )

        self.llm_provider = (
            LLMProvider()
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
                ),

                "provider": None,

                "model": None
            }

        # Build Context

        context = (
            self.context_builder.build(
                retrieval["facts"]
            )
        )

        # Build RAG Prompt

        prompt = (
            self.prompt_manager.build_prompt(
                query=query,
                context=context
            )
        )

        # Generate Response Using Gemini

        llm_response = (
            self.llm_provider.generate(
                prompt
            )
        )

        return {

            "retrieval": retrieval,

            "context": context,

            "prompt": prompt,

            "response": (
                llm_response.content
            ),

            "provider": (
                llm_response.provider
            ),

            "model": (
                llm_response.model
            )
        }
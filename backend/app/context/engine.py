from app.context.retriever import (
    ContextRetriever
)

from app.context.ranking import (
    ContextRanker
)

from app.context.summarizer import (
    ContextSummarizer
)


class ContextEngine:

    def __init__(self):

        self.retriever = (
            ContextRetriever()
        )

        self.ranker = (
            ContextRanker()
        )

        self.summarizer = (
            ContextSummarizer()
        )

    def get_context(
        self,
        query: str,
        messages: list
    ):

        retrieved = (
            self.retriever.retrieve(
                query,
                messages
            )
        )

        ranked = (
            self.ranker.rank(
                retrieved
            )
        )

        summary = (
            self.summarizer.summarize(
                ranked
            )
        )

        return summary
from app.research.models import (
    ResearchResult
)

from app.knowledge.retriever import (
    KnowledgeRetriever
)


class ResearchAgent:

    def __init__(self):

        self.retriever = (
            KnowledgeRetriever()
        )

    def research(
        self,
        query: str
    ):

        evidence = (
            self.retriever.retrieve(
                query
            )
        )

        if evidence:

            conclusion = (
                f"Found {len(evidence)} "
                f"relevant knowledge items."
            )

        else:

            conclusion = (
                "No relevant knowledge found."
            )

        return ResearchResult(
            query=query,
            evidence=evidence,
            conclusion=conclusion
        )
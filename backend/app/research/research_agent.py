"""Research agent: threshold-gated knowledge lookup with conclusions."""

from app.knowledge.retriever import KnowledgeRetriever
from app.research.models import ResearchResult


class ResearchAgent:
    def __init__(self, retriever: KnowledgeRetriever | None = None):
        self.retriever = retriever or KnowledgeRetriever()

    def research(self, query: str) -> ResearchResult:
        results = self.retriever.retrieve_many(query)
        if not results:
            return ResearchResult(
                query=query,
                evidence=[],
                conclusion="No relevant knowledge found for this query.",
                sources=[],
            )
        evidence: list[str] = []
        sources: list[str] = []
        for result in results:
            sources.append(result.topic)
            evidence.extend(result.facts)
        conclusion = (
            f"Found {len(evidence)} relevant facts across "
            f"{len(sources)} topic(s): {', '.join(sources)}."
        )
        return ResearchResult(query=query, evidence=evidence,
                              conclusion=conclusion, sources=sources)

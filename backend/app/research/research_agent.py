from app.research.models import (
    ResearchResult
)

from app.research.evidence_store import (
    EvidenceStore
)


class ResearchAgent:

    def __init__(self):

        self.store = EvidenceStore()

    def research(
        self,
        query: str
    ):

        if "AI" in query:

            self.store.add_evidence(
                "Python required"
            )

            self.store.add_evidence(
                "Git required"
            )

            self.store.add_evidence(
                "Portfolio required"
            )

        evidence = (
            self.store.get_evidence()
        )

        conclusion = (
            "Focus on Python, Git, "
            "and projects before applying."
        )

        return ResearchResult(
            query=query,
            evidence=evidence,
            conclusion=conclusion
        )
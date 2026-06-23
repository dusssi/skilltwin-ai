from app.research.evidence_store import (
    EvidenceStore
)

store = EvidenceStore()

store.add_evidence(
    "Python required"
)

store.add_evidence(
    "Git required"
)

print(
    store.get_evidence()
)
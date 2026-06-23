class EvidenceStore:

    def __init__(self):

        self.evidence = []

    def add_evidence(
        self,
        fact: str
    ):

        self.evidence.append(
            fact
        )

    def get_evidence(
        self
    ):

        return self.evidence
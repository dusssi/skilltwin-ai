from app.knowledge.knowledge_store import (
    KnowledgeStore
)


class KnowledgeRetriever:

    def __init__(self):

        self.store = KnowledgeStore()

    def retrieve(
        self,
        query: str
    ):

        items = self.store.get_all_items()

        for item in items:

            if query.lower() in item.topic.lower():

                return item.facts

        return []
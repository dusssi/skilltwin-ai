from app.knowledge.knowledge_store import (
    KnowledgeStore
)

store = KnowledgeStore()

items = store.get_all_items()

for item in items:

    print(item)
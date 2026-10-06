"""Unit tests for threshold-gated knowledge retrieval."""

from app.knowledge.retriever import KnowledgeRetriever
from app.knowledge.knowledge_store import KnowledgeStore


def test_relevant_query_returns_topic():
    result = KnowledgeRetriever().retrieve("How do I get an AI internship?")
    assert result is not None
    assert result.topic == "AI Internship"
    assert result.score >= 0.12
    assert len(result.facts) > 0


def test_irrelevant_query_returns_none():
    # Regression: legacy retriever always returned a topic.
    result = KnowledgeRetriever().retrieve("quantum banana astrophysics zebra")
    assert result is None


def test_empty_query_returns_none():
    assert KnowledgeRetriever().retrieve("") is None
    assert KnowledgeRetriever().retrieve("   ") is None


def test_retrieve_many_respects_threshold_and_order():
    results = KnowledgeRetriever().retrieve_many("docker containers and python")
    assert len(results) >= 1
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)
    assert all(score >= 0.12 for score in scores)


def test_runtime_documents_are_searchable():
    store = KnowledgeStore()
    store.add_document("Rust", ["Rust is memory safe", "Cargo is the build tool"])
    retriever = KnowledgeRetriever(store=store)
    result = retriever.retrieve("tell me about Rust memory safety and cargo")
    assert result is not None
    assert result.topic == "Rust"

"""Recommendation agent: gap-driven suggestions persisted per user."""

from app.recommendations.engine import RecommendationEngine


class RecommendationAgent:
    name = "recommendation_agent"

    def __init__(self):
        self.engine = RecommendationEngine()

    def run(self, user_id: str) -> dict:
        return self.engine.generate(user_id)

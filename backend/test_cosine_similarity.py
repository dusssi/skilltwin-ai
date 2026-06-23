from app.vector.similarity import (
    SimilarityEngine
)

engine = SimilarityEngine()

score = engine.calculate(
    [1, 2, 3],
    [3, 2, 1]
)

print(score)
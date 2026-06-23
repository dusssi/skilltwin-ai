from app.vector.similarity import (
    SimilarityEngine
)

engine = SimilarityEngine()

score = engine.calculate(
    [13, 326, 2],
    [14, 327, 2]
)

print(score)
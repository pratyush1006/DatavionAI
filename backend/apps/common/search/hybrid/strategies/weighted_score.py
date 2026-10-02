"""
Weighted score fusion strategy.
"""

from __future__ import annotations

from ..fusion import SearchFusion


class WeightedScoreStrategy:
    name = "weighted"

    def score(
        self,
        *,
        keyword_score: float,
        vector_score: float,
    ) -> float:

        return SearchFusion.weighted_score(
            keyword_score=keyword_score,
            vector_score=vector_score,
        )


__all__ = ("WeightedScoreStrategy",)

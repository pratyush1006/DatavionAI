"""
Reciprocal Rank Fusion strategy.
"""

from __future__ import annotations

from ..fusion import SearchFusion


class ReciprocalRankStrategy:
    name = "rrf"

    def score(
        self,
        *,
        keyword_rank: int,
        vector_rank: int,
    ) -> float:

        return SearchFusion.reciprocal_rank(
            keyword_rank=keyword_rank,
            vector_rank=vector_rank,
        )


__all__ = ("ReciprocalRankStrategy",)

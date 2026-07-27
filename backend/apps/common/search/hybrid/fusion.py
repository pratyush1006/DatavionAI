"""
DatavionOS Search Fusion Algorithms.

Supports:

- Reciprocal Rank Fusion
- Weighted score fusion
"""

from __future__ import annotations


class SearchFusion:
    """
    Combines multiple search signals.
    """

    @staticmethod
    def weighted_score(
        *,
        keyword_score: float,
        vector_score: float,
        keyword_weight: float = 0.3,
        vector_weight: float = 0.7,
    ) -> float:
        """
        Weighted score combination.
        """

        return keyword_score * keyword_weight + vector_score * vector_weight

    @staticmethod
    def reciprocal_rank(
        *,
        keyword_rank: int,
        vector_rank: int,
        k: int = 60,
    ) -> float:
        """
        Reciprocal Rank Fusion score.
        """

        return 1 / (k + keyword_rank) + 1 / (k + vector_rank)


__all__: tuple[str, ...] = ("SearchFusion",)

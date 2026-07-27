"""
Hybrid search ranking.

Combines:

- keyword score
- vector score
- business signals
"""

from __future__ import annotations

from typing import Any

from ..base import BaseRankingStrategy
from ..types import (
    RankingResult,
)


class HybridRankingStrategy(
    BaseRankingStrategy,
):
    name = "hybrid"

    def rank(
        self,
        *,
        items: list[Any],
        **kwargs: Any,
    ) -> RankingResult:

        return RankingResult(
            items=[],
            strategy=self.name,
            metadata={
                "keyword_weight": 0.3,
                "vector_weight": 0.7,
            },
        )


__all__ = ("HybridRankingStrategy",)

"""
Relevance ranking strategy.
"""

from __future__ import annotations

from typing import Any

from ..base import BaseRankingStrategy
from ..types import (
    RankingItem,
    RankingResult,
)


class RelevanceRankingStrategy(
    BaseRankingStrategy,
):
    name = "relevance"

    def rank(
        self,
        *,
        items: list[Any],
        **kwargs: Any,
    ) -> RankingResult:

        ranked = sorted(
            items,
            key=lambda item: getattr(
                item,
                "score",
                0,
            ),
            reverse=True,
        )

        return RankingResult(
            items=[
                RankingItem(
                    id=str(item.id),
                    score=getattr(
                        item,
                        "score",
                        0,
                    ),
                )
                for item in ranked
            ],
            strategy=self.name,
        )


__all__ = ("RelevanceRankingStrategy",)

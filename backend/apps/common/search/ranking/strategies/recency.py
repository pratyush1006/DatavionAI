"""
Recency ranking strategy.

Useful for:

- clinical timeline
- recent encounters
- audit events
"""

from __future__ import annotations

from typing import Any

from ..base import BaseRankingStrategy
from ..types import (
    RankingResult,
)


class RecencyRankingStrategy(
    BaseRankingStrategy,
):
    name = "recency"

    def rank(
        self,
        *,
        items: list[Any],
        **kwargs: Any,
    ) -> RankingResult:

        return RankingResult(
            items=[],
            strategy=self.name,
        )


__all__ = ("RecencyRankingStrategy",)

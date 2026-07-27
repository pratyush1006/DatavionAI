"""
DatavionOS Ranking Engine.

Unified ranking orchestration layer.

Supports:

- relevance ranking
- recency ranking
- hybrid ranking
- future AI reranking
"""

from __future__ import annotations

from typing import Any

from .base import (
    BaseRankingStrategy,
)
from .strategies.hybrid import (
    HybridRankingStrategy,
)
from .strategies.recency import (
    RecencyRankingStrategy,
)
from .strategies.relevance import (
    RelevanceRankingStrategy,
)
from .types import (
    RankingResult,
)


class RankingEngine:
    """
    Search ranking orchestrator.
    """

    def __init__(
        self,
    ) -> None:

        self._strategies: dict[
            str,
            BaseRankingStrategy,
        ] = {
            "hybrid": HybridRankingStrategy(),
            "relevance": RelevanceRankingStrategy(),
            "recency": RecencyRankingStrategy(),
        }

    def register(
        self,
        strategy: BaseRankingStrategy,
    ) -> None:
        """
        Register custom ranking strategy.
        """

        self._strategies[strategy.name] = strategy

    def rank(
        self,
        *,
        items: list[Any],
        strategy: str = "hybrid",
        **kwargs: Any,
    ) -> RankingResult:
        """
        Execute ranking strategy.
        """

        ranking_strategy = self._strategies.get(
            strategy,
        )

        if ranking_strategy is None:
            raise ValueError(f"Unknown ranking strategy '{strategy}'.")

        return ranking_strategy.rank(
            items=items,
            **kwargs,
        )


ranking_engine = RankingEngine()


__all__: tuple[str, ...] = (
    "RankingEngine",
    "ranking_engine",
)

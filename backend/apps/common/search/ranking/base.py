"""
DatavionOS Ranking Base Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .types import (
    RankingResult,
)


class BaseRankingStrategy(
    ABC,
):
    """
    Base ranking strategy.
    """

    name: str = ""

    @abstractmethod
    def rank(
        self,
        *,
        items: list[Any],
        **kwargs: Any,
    ) -> RankingResult:
        """
        Rank search results.
        """

        raise NotImplementedError


__all__: tuple[str, ...] = ("BaseRankingStrategy",)

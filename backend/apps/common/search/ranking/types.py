"""
DatavionOS Search Ranking Types.

Supports:

- Hybrid ranking
- Relevance scoring
- Recency scoring
- AI reranking
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class RankingItem:
    """
    Search result candidate.
    """

    id: str

    score: float = 0.0

    metadata: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class RankingResult:
    """
    Ranked search response.
    """

    items: list[RankingItem]

    strategy: str

    metadata: dict[str, Any] | None = None


__all__: tuple[str, ...] = (
    "RankingItem",
    "RankingResult",
)

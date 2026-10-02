"""
DatavionOS Hybrid Search Types.

Combines:

- keyword search results
- vector search results
- ranking signals
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class HybridSearchItem:
    """
    Unified search candidate.
    """

    id: str

    keyword_score: float = 0.0

    vector_score: float = 0.0

    final_score: float = 0.0

    metadata: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class HybridSearchResult:
    """
    Hybrid search response.
    """

    items: list[HybridSearchItem]

    strategy: str

    metadata: dict[str, Any] | None = None


__all__: tuple[str, ...] = (
    "HybridSearchItem",
    "HybridSearchResult",
)

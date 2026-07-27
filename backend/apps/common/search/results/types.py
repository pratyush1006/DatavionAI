"""
DatavionOS Search Result Types.

Standard response contracts for:

- REST APIs
- FHIR Bundles
- AI retrieval
- Infinite scrolling
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class SearchItem:
    """
    Normalized search item.
    """

    id: str

    score: float = 0.0

    content: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class SearchPagination:
    """
    Search pagination metadata.

    Cursor ready for:

    - infinite scrolling
    - FHIR Bundle paging
    - timeline feeds
    """

    page: int = 1

    page_size: int = 25

    total: int = 0

    total_pages: int = 0

    next_cursor: str | None = None

    previous_cursor: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class SearchResponse:
    """
    Unified DatavionOS search response.
    """

    items: list[SearchItem]

    total: int

    pagination: SearchPagination

    provider: str

    mode: str

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "SearchItem",
    "SearchPagination",
    "SearchResponse",
)

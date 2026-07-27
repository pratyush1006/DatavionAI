"""
DatavionOS Search Types.

Shared contracts for all search implementations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeAlias

SearchMetadata: TypeAlias = dict[str, Any]


SearchFilters: TypeAlias = dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
)
class SearchRequest:
    """
    Standard search request.
    """

    query: str

    tenant_id: str | None = None

    organization_id: str | None = None

    patient_id: str | None = None

    filters: SearchFilters | None = None

    page: int = 1

    page_size: int = 25


@dataclass(
    frozen=True,
    slots=True,
)
class SearchItem:
    """
    Individual search result.
    """

    id: str

    data: Any

    score: float | None = None

    metadata: SearchMetadata | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class SearchResult:
    """
    Standard search response.

    Supports:

    - API pagination
    - FHIR Bundle paging
    - AI retrieval ranking
    - timeline feeds
    """

    items: list[SearchItem]

    total: int

    page: int

    page_size: int

    total_pages: int

    metadata: SearchMetadata | None = None


__all__: tuple[str, ...] = (
    "SearchFilters",
    "SearchItem",
    "SearchMetadata",
    "SearchRequest",
    "SearchResult",
)

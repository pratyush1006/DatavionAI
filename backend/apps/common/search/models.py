"""
Search models for DatavionOS.

Defines immutable framework-level search objects.

These models describe search mechanics only.

Domain-specific indexing belongs to application modules:

- patients
- laboratories
- documents
- billing
- clinical
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)

from apps.common.search.constants import (
    DEFAULT_SEARCH_MODE,
)
from apps.common.search.types import (
    DocumentID,
    IndexName,
    SearchContext,
    SearchFilters,
    SearchMetadata,
    SearchQuery,
    SearchScore,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SearchDocument:
    """
    Search index document.

    Represents an indexed entity.
    """

    document_id: DocumentID

    index: IndexName

    content: str

    metadata: SearchMetadata = field(
        default_factory=dict,
    )

    tenant_id: str | int | None = None

    organization_id: str | int | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class SearchRequest:
    """
    Search request definition.
    """

    query: SearchQuery

    mode: str = DEFAULT_SEARCH_MODE

    filters: SearchFilters = field(
        default_factory=dict,
    )

    context: SearchContext = field(
        default_factory=dict,
    )

    limit: int = 50


@dataclass(
    frozen=True,
    slots=True,
)
class SearchResult:
    """
    Individual search result.
    """

    document_id: DocumentID

    score: SearchScore

    content: str

    metadata: SearchMetadata = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class SearchResponse:
    """
    Search operation response.
    """

    query: SearchQuery

    results: tuple[SearchResult, ...]

    total: int

    metadata: SearchMetadata = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "SearchDocument",
    "SearchRequest",
    "SearchResponse",
    "SearchResult",
)

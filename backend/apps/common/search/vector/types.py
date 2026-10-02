"""
DatavionOS Vector Search Types.

Shared contracts for all vector backends.

Supports:

- pgvector
- Pinecone
- ChromaDB
- FAISS
- Azure AI Search

Designed for:

- Healthcare timelines
- FHIR Bundle paging
- AI semantic retrieval
- RAG pipelines
- Enterprise search
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

type Vector = list[float]

type VectorMetadata = dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
)
class VectorDocument:
    """
    Document stored in vector index.

    Examples:

    - Clinical notes
    - Lab reports
    - Medical documents
    - Audit events
    - FHIR resources
    """

    id: str

    content: str

    vector: Vector

    metadata: VectorMetadata | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class VectorSearchRequest:
    """
    Vector similarity search request.

    Supports:

    - tenant isolation
    - organization isolation
    - patient scoped retrieval
    - metadata filtering
    """

    vector: Vector

    top_k: int = 10

    tenant_id: str | None = None

    organization_id: str | None = None

    patient_id: str | None = None

    filters: VectorMetadata | None = None

    cursor: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class VectorSearchItem:
    """
    Individual vector search result.
    """

    id: str

    content: str

    score: float

    metadata: VectorMetadata | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class VectorPagination:
    """
    Pagination metadata.

    Future compatible with:

    - FHIR Bundle paging
    - Infinite scrolling UI
    - Cursor pagination
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
class VectorSearchResult:
    """
    Standard vector search response.

    Used by:

    - AI assistants
    - RAG pipelines
    - Clinical timeline search
    - Healthcare knowledge retrieval
    """

    items: list[VectorSearchItem]

    total: int

    provider: str

    pagination: VectorPagination | None = None

    metadata: VectorMetadata | None = None


__all__: tuple[str, ...] = (
    "Vector",
    "VectorDocument",
    "VectorMetadata",
    "VectorPagination",
    "VectorSearchItem",
    "VectorSearchRequest",
    "VectorSearchResult",
)

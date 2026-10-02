"""
DatavionOS Vector Search Framework.

Public API for vector database abstraction.

Supports:

- pgvector
- Pinecone
- ChromaDB
- FAISS
- Azure AI Search
"""

from __future__ import annotations

from .base import (
    BaseVectorBackend,
)
from .engine import (
    VectorEngine,
    vector_engine,
)
from .providers import (
    register_default_vector_providers,
)
from .registry import (
    VECTOR_PROVIDERS,
    get_vector_provider,
    has_vector_provider,
    list_vector_providers,
    register_vector_provider,
    vector_provider,
)
from .service import (
    VectorSearchService,
    vector_search_service,
)
from .types import (
    Vector,
    VectorDocument,
    VectorMetadata,
    VectorSearchItem,
    VectorSearchRequest,
    VectorSearchResult,
)

__all__: tuple[str, ...] = (
    # Base
    "BaseVectorBackend",
    # Registry
    "VECTOR_PROVIDERS",
    "get_vector_provider",
    "has_vector_provider",
    "list_vector_providers",
    "register_vector_provider",
    "vector_provider",
    # Types
    "Vector",
    "VectorDocument",
    "VectorMetadata",
    "VectorSearchItem",
    "VectorSearchRequest",
    "VectorSearchResult",
    # Providers
    "register_default_vector_providers",
    "VectorEngine",
    "vector_engine",
    "VectorSearchService",
    "vector_search_service",
)

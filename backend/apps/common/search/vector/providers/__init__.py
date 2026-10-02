"""
DatavionOS Vector Providers.

Registers supported vector backends.

Supported:

- PostgreSQL pgvector
- Pinecone
- ChromaDB
- FAISS
- Azure AI Search
"""

from __future__ import annotations

from .azure_ai_search import (
    AzureAISearchBackend,
)
from .chromadb import (
    ChromaDBBackend,
)
from .faiss import (
    FAISSBackend,
)
from .pgvector import (
    PGVectorBackend,
)
from .pinecone import (
    PineconeBackend,
)


def register_default_vector_providers() -> None:
    """Keep no-op vector backends disabled until storage works.

    Each built-in adapter currently drops writes and returns empty results.
    Deployments can explicitly register an implemented backend.
    """

    return


register_default_vector_providers()


__all__: tuple[str, ...] = (
    "AzureAISearchBackend",
    "ChromaDBBackend",
    "FAISSBackend",
    "PGVectorBackend",
    "PineconeBackend",
    "register_default_vector_providers",
)

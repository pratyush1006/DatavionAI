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

from ..registry import (
    register_vector_provider,
)
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
    """
    Register built-in vector backends.
    """

    register_vector_provider(
        "pgvector",
        PGVectorBackend,
        overwrite=True,
    )

    register_vector_provider(
        "pinecone",
        PineconeBackend,
        overwrite=True,
    )

    register_vector_provider(
        "chromadb",
        ChromaDBBackend,
        overwrite=True,
    )

    register_vector_provider(
        "faiss",
        FAISSBackend,
        overwrite=True,
    )

    register_vector_provider(
        "azure_ai_search",
        AzureAISearchBackend,
        overwrite=True,
    )


register_default_vector_providers()


__all__: tuple[str, ...] = (
    "AzureAISearchBackend",
    "ChromaDBBackend",
    "FAISSBackend",
    "PGVectorBackend",
    "PineconeBackend",
    "register_default_vector_providers",
)

"""
DatavionOS Vector Backend Contract.

Defines the interface for all vector storage engines.

Supported backends:

- PostgreSQL pgvector
- Pinecone
- ChromaDB
- FAISS
- Azure AI Search
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .types import (
    VectorDocument,
    VectorSearchRequest,
    VectorSearchResult,
)


class BaseVectorBackend(
    ABC,
):
    """
    Abstract vector backend.

    All vector databases must implement
    this contract.
    """

    name: str = ""

    @abstractmethod
    def index(
        self,
        document: VectorDocument,
        **kwargs: Any,
    ) -> None:
        """
        Store vector document.
        """

        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        request: VectorSearchRequest,
        **kwargs: Any,
    ) -> VectorSearchResult:
        """
        Execute similarity search.
        """

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        document_id: str,
        **kwargs: Any,
    ) -> None:
        """
        Delete vector document.
        """

        raise NotImplementedError

    def health_check(
        self,
    ) -> bool:
        """
        Backend health status.
        """

        return True

    def supports_filtering(
        self,
    ) -> bool:
        """
        Metadata filtering support.

        Required for:

        - tenant isolation
        - organization filtering
        - patient scoped search
        """

        return False


__all__: tuple[str, ...] = ("BaseVectorBackend",)

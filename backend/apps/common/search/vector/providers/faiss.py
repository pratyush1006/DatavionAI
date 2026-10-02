"""
FAISS vector backend.
"""

from __future__ import annotations

from typing import Any

from ..base import BaseVectorBackend
from ..types import (
    VectorDocument,
    VectorSearchRequest,
    VectorSearchResult,
)


class FAISSBackend(
    BaseVectorBackend,
):
    name = "faiss"

    def index(
        self,
        document: VectorDocument,
        **kwargs: Any,
    ) -> None:
        return None

    def search(
        self,
        request: VectorSearchRequest,
        **kwargs: Any,
    ) -> VectorSearchResult:

        return VectorSearchResult(
            items=[],
            total=0,
            provider=self.name,
        )

    def delete(
        self,
        document_id: str,
        **kwargs: Any,
    ) -> None:
        return None


__all__ = ("FAISSBackend",)

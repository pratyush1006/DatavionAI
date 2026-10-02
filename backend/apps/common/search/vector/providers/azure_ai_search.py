"""
Azure AI Search vector backend.
"""

from __future__ import annotations

from typing import Any

from ..base import BaseVectorBackend
from ..types import (
    VectorDocument,
    VectorSearchRequest,
    VectorSearchResult,
)


class AzureAISearchBackend(
    BaseVectorBackend,
):
    name = "azure_ai_search"

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

    def supports_filtering(
        self,
    ) -> bool:
        return True


__all__ = ("AzureAISearchBackend",)

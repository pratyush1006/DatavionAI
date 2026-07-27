"""
Searchable interface for the DatavionOS platform.

Defines the contract for resources that can be transformed
into searchable representations.

Used by:

- Enterprise search
- OpenSearch / Elasticsearch indexing
- Vector databases
- RAG pipelines
- AI knowledge retrieval
"""

from __future__ import annotations

from typing import Protocol

from apps.core.types import JSONObject


class Searchable(
    Protocol,
):
    """
    Contract for searchable resources.

    Implementations should expose a normalized representation
    suitable for:

    - keyword indexing
    - semantic embeddings
    - AI retrieval pipelines
    - analytics search
    """

    def to_search_document(
        self,
    ) -> JSONObject:
        """
        Return the searchable document representation.

        Example:

            {
                "id": "...",
                "title": "...",
                "content": "...",
                "metadata": {}
            }

        Returns:
            JSON compatible search document.
        """
        ...


__all__: tuple[str, ...] = ("Searchable",)

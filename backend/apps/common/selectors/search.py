"""
DatavionOS Selector Search.

Enterprise search utilities.

Supports:

- Safe field search
- Multi-field search
- Configurable modes
- Future full-text integration
- AI semantic search extension
"""

from __future__ import annotations

from enum import StrEnum
from typing import TypeVar

from django.db.models import Model, Q, QuerySet

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


class SearchMode(StrEnum):
    """
    Supported search strategies.
    """

    CONTAINS = "contains"

    FULL_TEXT = "full_text"

    SEMANTIC = "semantic"


class Search:
    """
    Generic selector search helper.
    """

    MIN_QUERY_LENGTH = 2

    @classmethod
    def apply(
        cls,
        queryset: QuerySet[ModelType],
        *,
        query: str | None = None,
        fields: tuple[str, ...] = (),
        allowed_fields: tuple[str, ...] = (),
        mode: SearchMode = SearchMode.CONTAINS,
    ) -> QuerySet[ModelType]:
        """
        Apply search.
        """

        if not query:
            return queryset

        query = query.strip()

        if len(query) < cls.MIN_QUERY_LENGTH:
            return queryset

        if allowed_fields:
            fields = tuple(field for field in fields if field in allowed_fields)

        if not fields:
            return queryset

        if mode == SearchMode.CONTAINS:
            return cls.contains(
                queryset,
                query=query,
                fields=fields,
            )

        if mode == SearchMode.FULL_TEXT:
            return cls.full_text(
                queryset,
                query=query,
                fields=fields,
            )

        if mode == SearchMode.SEMANTIC:
            return cls.semantic(
                queryset,
                query=query,
            )

        return queryset

    @staticmethod
    def contains(
        queryset: QuerySet[ModelType],
        *,
        query: str,
        fields: tuple[str, ...],
    ) -> QuerySet[ModelType]:
        """
        Standard icontains search.
        """

        predicate = Q()

        for field in fields:
            predicate |= Q(
                **{
                    f"{field}__icontains": query,
                }
            )

        return queryset.filter(
            predicate,
        )

    @staticmethod
    def full_text(
        queryset: QuerySet[ModelType],
        *,
        query: str,
        fields: tuple[str, ...],
    ) -> QuerySet[ModelType]:
        """
        PostgreSQL full-text search extension.

        Implement per application.
        """

        return queryset

    @staticmethod
    def semantic(
        queryset: QuerySet[ModelType],
        *,
        query: str,
    ) -> QuerySet[ModelType]:
        """
        AI semantic search extension.

        Future integration:

        - Vector database
        - Embeddings
        - RAG
        """

        return queryset


__all__: tuple[str, ...] = (
    "Search",
    "SearchMode",
)

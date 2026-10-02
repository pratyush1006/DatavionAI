"""
Search configuration models for DatavionOS.

Provides immutable configuration objects used by the search
framework.

The configuration layer controls search behaviour without
coupling to a specific search provider.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.search.constants import (
    DEFAULT_BACKEND,
    DEFAULT_RANKING_STRATEGY,
    DEFAULT_SEARCH_MODE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SearchConfiguration:
    """
    Search framework configuration.

    Controls general search behaviour.
    """

    enabled: bool = True

    mode: str = DEFAULT_SEARCH_MODE

    backend: str = DEFAULT_BACKEND

    ranking_strategy: str = DEFAULT_RANKING_STRATEGY

    max_results: int = 50

    tenant_isolation: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class IndexConfiguration:
    """
    Search indexing configuration.

    Controls indexing behaviour.
    """

    enabled: bool = True

    async_indexing: bool = True

    update_on_change: bool = True

    delete_on_remove: bool = True

    store_metadata: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class SemanticSearchConfiguration:
    """
    AI semantic search configuration.

    Supports future RAG/vector search integration.
    """

    enabled: bool = True

    embedding_enabled: bool = True

    vector_backend: str = "vector"

    similarity_threshold: float = 0.75


DEFAULT_SEARCH_CONFIGURATION = SearchConfiguration()


DEFAULT_INDEX_CONFIGURATION = IndexConfiguration()


DEFAULT_SEMANTIC_SEARCH_CONFIGURATION = SemanticSearchConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_INDEX_CONFIGURATION",
    "DEFAULT_SEARCH_CONFIGURATION",
    "DEFAULT_SEMANTIC_SEARCH_CONFIGURATION",
    "IndexConfiguration",
    "SearchConfiguration",
    "SemanticSearchConfiguration",
)

"""
Search constants for DatavionOS.

Defines framework-wide constants for search modes,
indexing operations, and ranking strategies.
"""

from __future__ import annotations

###############################################################################
# Search Modes
###############################################################################

SEARCH_MODE_KEYWORD = "keyword"

SEARCH_MODE_SEMANTIC = "semantic"

SEARCH_MODE_HYBRID = "hybrid"


###############################################################################
# Index Operations
###############################################################################

INDEX_CREATE = "create"

INDEX_UPDATE = "update"

INDEX_DELETE = "delete"

INDEX_REBUILD = "rebuild"


###############################################################################
# Search Result Types
###############################################################################

RESULT_DOCUMENT = "document"

RESULT_RECORD = "record"

RESULT_ENTITY = "entity"


###############################################################################
# Ranking Strategies
###############################################################################

RANKING_RELEVANCE = "relevance"

RANKING_RECENCY = "recency"

RANKING_WEIGHTED = "weighted"

RANKING_SEMANTIC = "semantic"


###############################################################################
# Backend Types
###############################################################################

BACKEND_DATABASE = "database"

BACKEND_ELASTICSEARCH = "elasticsearch"

BACKEND_OPENSEARCH = "opensearch"

BACKEND_VECTOR = "vector"


###############################################################################
# Default Values
###############################################################################

DEFAULT_SEARCH_MODE = SEARCH_MODE_HYBRID

DEFAULT_RANKING_STRATEGY = RANKING_RELEVANCE

DEFAULT_BACKEND = BACKEND_DATABASE


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "BACKEND_DATABASE",
    "BACKEND_ELASTICSEARCH",
    "BACKEND_OPENSEARCH",
    "BACKEND_VECTOR",
    "DEFAULT_BACKEND",
    "DEFAULT_RANKING_STRATEGY",
    "DEFAULT_SEARCH_MODE",
    "INDEX_CREATE",
    "INDEX_DELETE",
    "INDEX_REBUILD",
    "INDEX_UPDATE",
    "RANKING_RECENCY",
    "RANKING_RELEVANCE",
    "RANKING_SEMANTIC",
    "RANKING_WEIGHTED",
    "RESULT_DOCUMENT",
    "RESULT_ENTITY",
    "RESULT_RECORD",
    "SEARCH_MODE_HYBRID",
    "SEARCH_MODE_KEYWORD",
    "SEARCH_MODE_SEMANTIC",
)

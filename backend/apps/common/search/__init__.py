"""
DatavionOS AI Search Framework.

Provides unified enterprise search abstraction for:

- Database search
- Full text search
- Vector search
- Hybrid search
- Semantic retrieval
- AI ranking
- RAG pipelines
"""

from __future__ import annotations

# ============================================================================
# Core Search Engine
# ============================================================================
from .engine import (
    SearchEngine,
    search_engine,
)

# ============================================================================
# Hybrid Search
# ============================================================================
from .hybrid import (
    HybridSearchEngine,
    HybridSearchItem,
    HybridSearchResult,
    SearchFusion,
    hybrid_search_engine,
)

# ============================================================================
# Document Indexing
# ============================================================================
from .indexer import (
    DocumentChunk,
    DocumentIndexer,
    document_indexer,
)

# ============================================================================
# Search Providers
# ============================================================================
from .providers import (
    PostgreSQLSearchProvider,
    VectorSearchProvider,
)
from .providers.registry import (
    register_default_search_providers,
)

# ============================================================================
# Ranking
# ============================================================================
from .ranking import (
    BaseRankingStrategy,
    HybridRankingStrategy,
    RankingEngine,
    RankingItem,
    RankingResult,
    RecencyRankingStrategy,
    RelevanceRankingStrategy,
    ranking_engine,
)

# ============================================================================
# Search Registry
# ============================================================================
from .registry import (
    SEARCH_PROVIDERS,
    get_search_provider,
    register_search_provider,
    search_provider,
)

# ============================================================================
# Unified Search Service
# ============================================================================
from .service import (
    SearchService,
    search_service,
)

# Register built-in providers.

register_default_search_providers()


__all__: tuple[str, ...] = (
    # ------------------------------------------------------------------------
    # Core Search
    # ------------------------------------------------------------------------
    "SearchEngine",
    "search_engine",
    # ------------------------------------------------------------------------
    # Registry
    # ------------------------------------------------------------------------
    "SEARCH_PROVIDERS",
    "get_search_provider",
    "register_search_provider",
    "search_provider",
    # ------------------------------------------------------------------------
    # Providers
    # ------------------------------------------------------------------------
    "PostgreSQLSearchProvider",
    "VectorSearchProvider",
    "register_default_search_providers",
    # ------------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------------
    "DocumentChunk",
    "DocumentIndexer",
    "document_indexer",
    # ------------------------------------------------------------------------
    # Unified Search Service
    # ------------------------------------------------------------------------
    "SearchService",
    "search_service",
    # ------------------------------------------------------------------------
    # Hybrid Search
    # ------------------------------------------------------------------------
    "HybridSearchEngine",
    "HybridSearchItem",
    "HybridSearchResult",
    "SearchFusion",
    "hybrid_search_engine",
    # ------------------------------------------------------------------------
    # Ranking
    # ------------------------------------------------------------------------
    "BaseRankingStrategy",
    "RankingEngine",
    "RankingItem",
    "RankingResult",
    "RelevanceRankingStrategy",
    "RecencyRankingStrategy",
    "HybridRankingStrategy",
    "ranking_engine",
)

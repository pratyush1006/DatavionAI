"""
DatavionOS Search Ranking Framework.

Provides enterprise search ranking.

Supports:

- relevance scoring
- recency ranking
- hybrid ranking
- future AI reranking
"""

from __future__ import annotations

from .base import (
    BaseRankingStrategy,
)
from .engine import (
    RankingEngine,
    ranking_engine,
)
from .strategies.hybrid import (
    HybridRankingStrategy,
)
from .strategies.recency import (
    RecencyRankingStrategy,
)
from .strategies.relevance import (
    RelevanceRankingStrategy,
)
from .types import (
    RankingItem,
    RankingResult,
)

__all__: tuple[str, ...] = (
    # Base
    "BaseRankingStrategy",
    # Engine
    "RankingEngine",
    "ranking_engine",
    # Types
    "RankingItem",
    "RankingResult",
    # Strategies
    "HybridRankingStrategy",
    "RelevanceRankingStrategy",
    "RecencyRankingStrategy",
)

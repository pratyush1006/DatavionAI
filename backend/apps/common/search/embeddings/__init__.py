"""
DatavionOS Embedding Framework.
"""

from __future__ import annotations

from .engine import (
    EmbeddingEngine,
    embedding_engine,
)
from .providers.registry import (
    register_default_embedding_providers,
)
from .registry import (
    EMBEDDING_PROVIDERS,
    get_embedding_provider,
    register_embedding_provider,
)
from .service import (
    EmbeddingService,
    embedding_service,
)

register_default_embedding_providers()


__all__ = (
    "EMBEDDING_PROVIDERS",
    "get_embedding_provider",
    "register_embedding_provider",
    "register_default_embedding_providers",
    "EmbeddingEngine",
    "embedding_engine",
    "EmbeddingService",
    "embedding_service",
)

"""
DatavionOS Embedding Providers.
"""

from __future__ import annotations

from .openai import (
    OpenAIEmbeddingProvider,
)

__all__: tuple[str, ...] = ("OpenAIEmbeddingProvider",)

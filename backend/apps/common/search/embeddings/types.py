"""
DatavionOS Embedding Types.

Shared type definitions for embedding providers.
"""

from __future__ import annotations

from typing import Any, TypeAlias

EmbeddingVector: TypeAlias = list[float]


EmbeddingBatch: TypeAlias = list[EmbeddingVector]


EmbeddingMetadata: TypeAlias = dict[
    str,
    Any,
]


__all__: tuple[str, ...] = (
    "EmbeddingVector",
    "EmbeddingBatch",
    "EmbeddingMetadata",
)

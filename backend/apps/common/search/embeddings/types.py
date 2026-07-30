"""
DatavionOS Embedding Types.

Shared type definitions for embedding providers.
"""

from __future__ import annotations

from typing import Any

type EmbeddingVector = list[float]


type EmbeddingBatch = list[EmbeddingVector]


type EmbeddingMetadata = dict[
    str,
    Any,
]


__all__: tuple[str, ...] = (
    "EmbeddingVector",
    "EmbeddingBatch",
    "EmbeddingMetadata",
)

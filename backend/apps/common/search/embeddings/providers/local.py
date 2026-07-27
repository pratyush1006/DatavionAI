"""
DatavionOS Local Embedding Provider.

Development/testing embedding backend.

Used for:

- pipeline testing
- CI tests
- local development
- offline environments
"""

from __future__ import annotations

import hashlib

from ..base import (
    BaseEmbeddingProvider,
)
from ..types import (
    EmbeddingBatch,
    EmbeddingVector,
)


class LocalEmbeddingProvider(
    BaseEmbeddingProvider,
):
    """
    Deterministic local embedding generator.
    """

    name = "local"

    model = "local-hash-embedding"

    dimensions = 8

    def embed(
        self,
        *,
        text: str,
        **kwargs,
    ) -> EmbeddingVector:
        """
        Generate deterministic vector.
        """

        digest = hashlib.sha256(
            text.encode("utf-8"),
        ).digest()

        return [value / 255 for value in digest[: self.dimensions]]

    def embed_batch(
        self,
        *,
        texts: list[str],
        **kwargs,
    ) -> EmbeddingBatch:
        """
        Generate batch embeddings.
        """

        return [
            self.embed(
                text=text,
            )
            for text in texts
        ]


__all__: tuple[str, ...] = ("LocalEmbeddingProvider",)

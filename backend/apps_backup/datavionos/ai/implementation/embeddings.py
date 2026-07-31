"""
Concrete embedding model implementation.
"""

from __future__ import annotations

import hashlib
import math
import os

from apps.datavionos.ai.embeddings import (
    Embedding,
    EmbeddingRequest,
    EmbeddingResponse,
)
from apps.datavionos.ai.exceptions import EmbeddingModelError


class OpenAIEmbeddingModel:
    """
    Embedding model backed by an OpenAI-compatible API.

    When no API key is configured a deterministic hashed bag-of-words vector
    is produced so retrieval pipelines remain functional offline.
    """

    DIMENSION = 1536

    def __init__(
        self,
        *,
        model: str = "text-embedding-3-small",
        api_key: str | None = None,
        base_url: str | None = None,
        dimension: int | None = None,
    ) -> None:
        self._model = model
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        self._dimension = dimension or self.DIMENSION

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """Generate embeddings for the supplied input."""

        if not self._api_key:
            return EmbeddingResponse(
                embeddings=tuple(
                    self._offline_embedding(text) for text in request.input
                ),
                metadata={"offline": True},
            )

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
            )

            response = await client.embeddings.create(
                model=self._model,
                input=list(request.input),
            )

            return EmbeddingResponse(
                embeddings=tuple(
                    Embedding(
                        input=item.input,
                        vector=tuple(float(x) for x in item.embedding),
                        metadata=request.metadata,
                    )
                    for item in response.data
                ),
                metadata={"model": self._model},
            )
        except Exception as exc:  # noqa: BLE001
            raise EmbeddingModelError(str(exc)) from exc

    def _offline_embedding(
        self,
        text: str,
    ) -> Embedding:
        vector = [0.0] * self._dimension
        tokens = text.lower().split()

        for token in tokens:
            hashed = hashlib.md5(token.encode("utf-8")).digest()
            index = int.from_bytes(hashed[:4], "big") % self._dimension
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        vector = [value / norm for value in vector]

        return Embedding(
            input=text,
            vector=tuple(vector),
            metadata={"offline": True},
        )


__all__ = [
    "OpenAIEmbeddingModel",
]

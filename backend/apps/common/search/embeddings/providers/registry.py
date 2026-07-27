"""
Default DatavionOS embedding provider registration.
"""

from __future__ import annotations

from apps.common.search.embeddings.registry import (
    register_embedding_provider,
)

from .azure import AzureEmbeddingProvider
from .huggingface import HuggingFaceEmbeddingProvider
from .local import (
    LocalEmbeddingProvider,
)
from .openai import OpenAIEmbeddingProvider


def register_default_embedding_providers() -> None:
    """
    Register built-in embedding providers.
    """

    register_embedding_provider(
        "openai",
        OpenAIEmbeddingProvider,
        overwrite=True,
    )

    register_embedding_provider(
        "azure",
        AzureEmbeddingProvider,
        overwrite=True,
    )

    register_embedding_provider(
        "huggingface",
        HuggingFaceEmbeddingProvider,
        overwrite=True,
    )
    register_embedding_provider(
        "local",
        LocalEmbeddingProvider,
        overwrite=True,
    )


__all__: tuple[str, ...] = ("register_default_embedding_providers",)

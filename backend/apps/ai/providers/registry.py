"""Provider registry and dependency boundary."""

from __future__ import annotations

from apps.ai.providers.implementation.embeddings import (
    MockEmbeddingProvider,
    OpenAIEmbeddingProvider,
)
from apps.ai.providers.implementation.mock import MockProvider
from apps.ai.providers.implementation.openai import OpenAIProvider

CHAT_PROVIDERS = {"mock": MockProvider, "openai": OpenAIProvider}
EMBEDDING_PROVIDERS = {"mock": MockEmbeddingProvider, "openai": OpenAIEmbeddingProvider}


def get_chat_provider(name: str, **kwargs):
    try:
        return CHAT_PROVIDERS[name](**kwargs)
    except KeyError as exc:
        raise ValueError(f"Unsupported AI chat provider: {name}") from exc


def get_embedding_provider(name: str, **kwargs):
    try:
        return EMBEDDING_PROVIDERS[name](**kwargs)
    except KeyError as exc:
        raise ValueError(f"Unsupported AI embedding provider: {name}") from exc

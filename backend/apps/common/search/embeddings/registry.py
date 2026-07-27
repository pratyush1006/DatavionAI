"""
DatavionOS Embedding Provider Registry.

Central registry for AI embedding providers.

Supports:

- OpenAI embeddings
- Azure OpenAI embeddings
- HuggingFace embeddings
- Future Gemini/custom providers

Design Principles:

- Lightweight
- Provider independent
- Thread safe registration
- Immutable public registry
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from .base import BaseEmbeddingProvider

###############################################################################
# Registry Storage
###############################################################################

_EMBEDDING_PROVIDERS: dict[
    str,
    type[BaseEmbeddingProvider],
] = {}


EMBEDDING_PROVIDERS: Final[
    MappingProxyType[
        str,
        type[BaseEmbeddingProvider],
    ]
] = MappingProxyType(
    _EMBEDDING_PROVIDERS,
)


###############################################################################
# Registration
###############################################################################


def register_embedding_provider(
    name: str,
    provider_class: type[BaseEmbeddingProvider],
    *,
    overwrite: bool = False,
) -> None:
    """
    Register an embedding provider.
    """

    if not overwrite and name in _EMBEDDING_PROVIDERS:
        raise ValueError(f"Embedding provider '{name}' is already registered.")

    _EMBEDDING_PROVIDERS[name] = provider_class


###############################################################################
# Lookup
###############################################################################


def get_embedding_provider(
    name: str,
) -> type[BaseEmbeddingProvider]:
    """
    Return registered embedding provider.
    """

    try:
        return _EMBEDDING_PROVIDERS[name]

    except KeyError as exc:
        raise LookupError(f"Unknown embedding provider '{name}'.") from exc


def has_embedding_provider(
    name: str,
) -> bool:
    """
    Check whether provider exists.
    """

    return name in _EMBEDDING_PROVIDERS


def unregister_embedding_provider(
    name: str,
) -> None:
    """
    Remove provider registration.
    """

    _EMBEDDING_PROVIDERS.pop(
        name,
        None,
    )


def list_embedding_providers() -> tuple[str, ...]:
    """
    Return registered provider names.
    """

    return tuple(
        sorted(
            _EMBEDDING_PROVIDERS.keys(),
        )
    )


###############################################################################
# Decorator
###############################################################################


def embedding_provider(
    name: str,
):
    """
    Decorator for embedding provider registration.
    """

    def decorator(
        cls: type[BaseEmbeddingProvider],
    ) -> type[BaseEmbeddingProvider]:

        register_embedding_provider(
            name,
            cls,
        )

        return cls

    return decorator


__all__: tuple[str, ...] = (
    "EMBEDDING_PROVIDERS",
    "embedding_provider",
    "get_embedding_provider",
    "has_embedding_provider",
    "list_embedding_providers",
    "register_embedding_provider",
    "unregister_embedding_provider",
)

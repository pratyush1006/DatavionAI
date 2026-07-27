"""
DatavionOS Vector Backend Registry.

Central registry for vector database backends.

Supports:

- pgvector
- Pinecone
- ChromaDB
- FAISS
- Azure AI Search
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from .base import (
    BaseVectorBackend,
)

_VECTOR_PROVIDERS: dict[
    str,
    type[BaseVectorBackend],
] = {}


VECTOR_PROVIDERS: Final = MappingProxyType(
    _VECTOR_PROVIDERS,
)


def register_vector_provider(
    name: str,
    backend: type[BaseVectorBackend],
    *,
    overwrite: bool = False,
) -> None:
    """
    Register vector backend.
    """

    if not overwrite and name in _VECTOR_PROVIDERS:
        raise ValueError(f"Vector provider '{name}' already registered.")

    _VECTOR_PROVIDERS[name] = backend


def get_vector_provider(
    name: str,
) -> type[BaseVectorBackend]:
    """
    Get vector backend class.
    """

    try:
        return _VECTOR_PROVIDERS[name]

    except KeyError as exc:
        raise LookupError(f"Unknown vector provider '{name}'.") from exc


def has_vector_provider(
    name: str,
) -> bool:
    """
    Check provider existence.
    """

    return name in _VECTOR_PROVIDERS


def list_vector_providers() -> tuple[str, ...]:
    """
    Return registered providers.
    """

    return tuple(
        sorted(
            _VECTOR_PROVIDERS.keys(),
        )
    )


def vector_provider(
    name: str,
):
    """
    Decorator for backend registration.
    """

    def decorator(
        cls: type[BaseVectorBackend],
    ):
        register_vector_provider(
            name,
            cls,
        )

        return cls

    return decorator


__all__: tuple[str, ...] = (
    "VECTOR_PROVIDERS",
    "get_vector_provider",
    "has_vector_provider",
    "list_vector_providers",
    "register_vector_provider",
    "vector_provider",
)

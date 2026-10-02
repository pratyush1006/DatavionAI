"""
DatavionOS Search Provider Registry.
"""

from __future__ import annotations

from collections.abc import Callable
from types import MappingProxyType
from typing import Final, TypeVar

from .exceptions import SearchProviderNotFoundError
from .providers.base import BaseSearchProvider

_SEARCH_PROVIDERS: dict[
    str,
    type[BaseSearchProvider],
] = {}

SearchProviderType = TypeVar("SearchProviderType", bound=BaseSearchProvider)


SEARCH_PROVIDERS: Final = MappingProxyType(
    _SEARCH_PROVIDERS,
)


def register_search_provider(
    name: str,
    provider: type[BaseSearchProvider],
    *,
    overwrite: bool = False,
) -> None:
    """
    Register search provider.
    """

    if not overwrite and name in _SEARCH_PROVIDERS:
        raise ValueError(f"Provider '{name}' already registered.")

    _SEARCH_PROVIDERS[name] = provider


def get_search_provider(
    name: str,
) -> type[BaseSearchProvider]:
    """
    Retrieve provider.
    """

    try:
        return _SEARCH_PROVIDERS[name]
    except KeyError as exc:
        raise SearchProviderNotFoundError(
            f"Search provider '{name}' is not configured for this deployment."
        ) from exc


def search_provider(
    name: str,
) -> Callable[[type[SearchProviderType]], type[SearchProviderType]]:
    """
    Provider decorator.
    """

    def decorator(
        cls: type[SearchProviderType],
    ) -> type[SearchProviderType]:

        register_search_provider(
            name,
            cls,
        )

        return cls

    return decorator


__all__ = (
    "SEARCH_PROVIDERS",
    "get_search_provider",
    "register_search_provider",
    "search_provider",
)

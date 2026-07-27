"""
DatavionOS Search Provider Registry.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from .providers.base import BaseSearchProvider

_SEARCH_PROVIDERS: dict[
    str,
    type[BaseSearchProvider],
] = {}


SEARCH_PROVIDERS: Final = MappingProxyType(
    _SEARCH_PROVIDERS,
)


def register_search_provider(
    name: str,
    provider: type[BaseSearchProvider],
    *,
    overwrite: bool = False,
):
    """
    Register search provider.
    """

    if not overwrite and name in _SEARCH_PROVIDERS:
        raise ValueError(f"Provider '{name}' already registered.")

    _SEARCH_PROVIDERS[name] = provider


def get_search_provider(
    name: str,
):
    """
    Retrieve provider.
    """

    return _SEARCH_PROVIDERS[name]


def search_provider(
    name: str,
):
    """
    Provider decorator.
    """

    def decorator(
        cls,
    ):

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

"""
Default DatavionOS search provider registration.
"""

from __future__ import annotations

from apps.common.search.registry import (
    register_search_provider,
)

from .postgres import (
    PostgreSQLSearchProvider,
)
from .vector import (
    VectorSearchProvider,
)


def register_default_search_providers() -> None:
    """
    Register built-in search providers.
    """

    register_search_provider(
        "postgres",
        PostgreSQLSearchProvider,
        overwrite=True,
    )

    register_search_provider(
        "vector",
        VectorSearchProvider,
        overwrite=True,
    )


__all__: tuple[str, ...] = ("register_default_search_providers",)

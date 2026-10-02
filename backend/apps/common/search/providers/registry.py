"""
Default DatavionOS search provider registration.
"""

from __future__ import annotations


def register_default_search_providers() -> None:
    """Keep no-op providers disabled until backed by real storage.

    Deployment specific implementations can register through the provider
    registry. The former built-ins always returned empty results, which made
    unavailable search look successful.
    """

    return


__all__: tuple[str, ...] = ("register_default_search_providers",)

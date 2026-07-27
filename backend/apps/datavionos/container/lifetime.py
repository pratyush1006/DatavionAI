"""
DatavionOS Service Lifetimes.
"""

from __future__ import annotations

from enum import (
    Enum,
    unique,
)


@unique
class ServiceLifetime(
    Enum,
):
    """
    Supported dependency injection
    service lifetimes.
    """

    SINGLETON = "singleton"
    SCOPED = "scoped"
    TRANSIENT = "transient"

    @property
    def is_singleton(
        self,
    ) -> bool:
        """
        Whether this lifetime is singleton.
        """

        return self is ServiceLifetime.SINGLETON

    @property
    def is_scoped(
        self,
    ) -> bool:
        """
        Whether this lifetime is scoped.
        """

        return self is ServiceLifetime.SCOPED

    @property
    def is_transient(
        self,
    ) -> bool:
        """
        Whether this lifetime is transient.
        """

        return self is ServiceLifetime.TRANSIENT

    @property
    def requires_scope(
        self,
    ) -> bool:
        """
        Whether resolution requires
        an active scope.
        """

        return self.is_scoped

    @property
    def is_cacheable(
        self,
    ) -> bool:
        """
        Indicates whether resolved
        instances may be cached.
        """

        return self in (
            ServiceLifetime.SINGLETON,
            ServiceLifetime.SCOPED,
        )

    def __str__(
        self,
    ) -> str:
        return self.value


def is_singleton(
    lifetime: ServiceLifetime,
) -> bool:
    """
    Determine whether a lifetime
    is singleton.
    """

    return lifetime.is_singleton


def is_scoped(
    lifetime: ServiceLifetime,
) -> bool:
    """
    Determine whether a lifetime
    is scoped.
    """

    return lifetime.is_scoped


def is_transient(
    lifetime: ServiceLifetime,
) -> bool:
    """
    Determine whether a lifetime
    is transient.
    """

    return lifetime.is_transient


def requires_scope(
    lifetime: ServiceLifetime,
) -> bool:
    """
    Determine whether a lifetime
    requires a scope.
    """

    return lifetime.requires_scope


def is_cacheable(
    lifetime: ServiceLifetime,
) -> bool:
    """
    Determine whether resolved
    instances should be cached.
    """

    return lifetime.is_cacheable


__all__ = [
    "ServiceLifetime",
    "is_singleton",
    "is_scoped",
    "is_transient",
    "requires_scope",
    "is_cacheable",
]

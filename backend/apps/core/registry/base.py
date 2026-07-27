"""
Base registry implementation for the DatavionOS platform.

Provides a reusable in-memory registry kernel used by:

- Module registry
- Feature registry
- Permission registry
- Provider registry

The registry layer is infrastructure only and contains no
business logic.
"""

from __future__ import annotations

from threading import RLock
from typing import Generic, TypeVar

T = TypeVar(
    "T",
)


class RegistryAlreadyRegisteredError(
    Exception,
):
    """
    Raised when attempting to register an existing key.
    """


class RegistryNotFoundError(
    Exception,
):
    """
    Raised when requested registry item does not exist.
    """


class Registry(
    Generic[T],
):
    """
    Generic enterprise registry.

    Supports:

    - Registration
    - Lookup
    - Discovery
    - Removal
    - Thread-safe mutation
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._registry: dict[str, T] = {}

        self._lock = RLock()

    def register(
        self,
        key: str,
        value: T,
    ) -> None:
        """
        Register a value.

        Raises:
            RegistryAlreadyRegisteredError
        """

        with self._lock:
            if key in self._registry:
                raise RegistryAlreadyRegisteredError(
                    f"'{key}' is already registered.",
                )

            self._registry[key] = value

    def unregister(
        self,
        key: str,
    ) -> None:
        """
        Remove a registered value.
        """

        with self._lock:
            self._registry.pop(
                key,
                None,
            )

    def get(
        self,
        key: str,
    ) -> T:
        """
        Retrieve a registered value.

        Raises:
            RegistryNotFoundError
        """

        try:
            return self._registry[key]

        except KeyError as exc:
            raise RegistryNotFoundError(
                f"'{key}' is not registered.",
            ) from exc

    def has(
        self,
        key: str,
    ) -> bool:
        """
        Check registration existence.
        """

        return key in self._registry

    def clear(
        self,
    ) -> None:
        """
        Remove all registrations.
        """

        with self._lock:
            self._registry.clear()

    def all(
        self,
    ) -> tuple[T, ...]:
        """
        Return all registered values.
        """

        return tuple(
            self._registry.values(),
        )

    def items(
        self,
    ) -> tuple[tuple[str, T], ...]:
        """
        Return all registry entries.
        """

        return tuple(
            self._registry.items(),
        )

    def __len__(
        self,
    ) -> int:
        """
        Return registry size.
        """

        return len(
            self._registry,
        )


__all__: tuple[str, ...] = (
    "Registry",
    "RegistryAlreadyRegisteredError",
    "RegistryNotFoundError",
)

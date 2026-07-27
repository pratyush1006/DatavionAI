"""
Concrete registry implementation for DatavionOS.

This module provides the default registry implementation built on top of
BaseRegistry. It is intended to be used by higher-level registries
throughout the platform.
"""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from typing import Generic, TypeVar

from apps.datavionos.exceptions import RegistryError

from .base import BaseRegistry

K = TypeVar(
    "K",
    bound=Hashable,
)

T = TypeVar("T")


class Registry(
    BaseRegistry[K, T],
    Generic[K, T],
):
    """
    Default registry implementation.

    This class extends BaseRegistry and provides additional
    convenience methods used by specialized registries.
    """

    def __init__(
        self,
        *,
        name: str,
    ) -> None:
        super().__init__(
            name=name,
        )

    # ------------------------------------------------------------------
    # Bulk Operations
    # ------------------------------------------------------------------

    def update(
        self,
        entries: Mapping[K, T],
    ) -> None:
        """
        Register multiple entries.

        Existing keys are rejected.
        """
        self.register_many(
            entries,
        )

    def replace(
        self,
        *,
        key: K,
        value: T,
    ) -> T:
        """
        Replace an existing entry.

        Raises:
            RegistryError:
                If the key does not exist.
        """
        with self._lock:
            if key not in self._entries:
                raise RegistryError(
                    message=f"{key!r} is not registered.",
                    error_code="REGISTRY_NOT_FOUND",
                )

            self._before_unregister(
                key=key,
                value=self._entries[key],
            )

            self._entries[key] = value

            self._after_register(
                key=key,
                value=value,
            )

            return value

    def upsert(
        self,
        *,
        key: K,
        value: T,
    ) -> T:
        """
        Insert or replace an entry.
        """
        with self._lock:
            if key in self._entries:
                self._entries[key] = value
                return value

            return self.register(
                key=key,
                value=value,
            )

    # ------------------------------------------------------------------
    # Query Operations
    # ------------------------------------------------------------------

    def first(self) -> T | None:
        """
        Return the first registered value.
        """
        for value in self._entries.values():
            return value

        return None

    def last(self) -> T | None:
        """
        Return the last registered value.
        """
        if not self._entries:
            return None

        return next(
            reversed(
                self._entries.values(),
            ),
        )

    def find(
        self,
        predicate,
    ) -> T | None:
        """
        Find the first matching entry.
        """
        for value in self._entries.values():
            if predicate(value):
                return value

        return None

    def filter(
        self,
        predicate,
    ) -> list[T]:
        """
        Return all matching entries.
        """
        return [value for value in self._entries.values() if predicate(value)]

    def map(
        self,
        function,
    ) -> list:
        """
        Apply a function to every registered value.
        """
        return [function(value) for value in self._entries.values()]

        # ------------------------------------------------------------------

    # Removal Operations
    # ------------------------------------------------------------------

    def pop(
        self,
        key: K,
        default: T | None = None,
    ) -> T | None:
        """
        Remove and return an entry.

        If the key does not exist, return the supplied default.
        """
        with self._lock:
            if key not in self._entries:
                return default

            return self.unregister(
                key,
            )

    def popitem(
        self,
    ) -> tuple[K, T]:
        """
        Remove and return the most recently registered entry.

        Raises:
            RegistryError:
                If the registry is empty.
        """
        with self._lock:
            if self.is_empty:
                raise RegistryError(
                    message="Registry is empty.",
                    error_code="REGISTRY_EMPTY",
                )

            key = next(
                reversed(
                    self._entries.keys(),
                ),
            )

            value = self.unregister(
                key,
            )

            return key, value

    # ------------------------------------------------------------------
    # Merge Operations
    # ------------------------------------------------------------------

    def merge(
        self,
        other: Mapping[K, T],
    ) -> None:
        """
        Merge another mapping into this registry.

        Existing keys are preserved.
        """
        for key, value in other.items():
            if key not in self:
                self.register(
                    key=key,
                    value=value,
                )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Remove every registered entry.
        """
        self.clear()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate registry integrity.

        Raises:
            RegistryError:
                If duplicate keys are detected.
        """
        keys = tuple(
            self._entries.keys(),
        )

        if len(keys) != len(set(keys)):
            raise RegistryError(
                message="Duplicate registry keys detected.",
                error_code="REGISTRY_DUPLICATE",
            )

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __copy__(
        self,
    ) -> Registry[K, T]:
        """
        Return a shallow registry copy.
        """
        registry = Registry[K, T](
            name=self.name,
        )

        registry.register_many(
            self.copy(),
        )

        return registry

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """
        return f"{type(self).__name__}(name={self.name!r}, size={self.size})"


__all__ = [
    "Registry",
]

"""
Base registry implementation for DatavionOS.

This module provides the generic, thread-safe registry infrastructure used
throughout the DatavionOS platform.
"""

from __future__ import annotations

from abc import ABC
from collections import OrderedDict
from collections.abc import Hashable, Iterable, Iterator, Mapping
from threading import RLock
from types import MappingProxyType
from typing import TypeVar

from apps.datavionos.exceptions import RegistryError
from apps.datavionos.types import Metadata

K = TypeVar(
    "K",
    bound=Hashable,
)

T = TypeVar("T")


class BaseRegistry[K: Hashable, T](
    ABC,
):
    """
    Generic thread-safe registry.

    This class serves as the foundation for every registry within
    DatavionOS including modules, plugins, services, capabilities,
    workflows and event handlers.
    """

    def __init__(
        self,
        *,
        name: str,
    ) -> None:
        """
        Initialize the registry.

        Args:
            name:
                Human-readable registry name.
        """
        self._name = name
        self._lock = RLock()
        self._entries: OrderedDict[K, T] = OrderedDict()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Registry name.
        """
        return self._name

    @property
    def size(self) -> int:
        """
        Number of registered entries.
        """
        return len(self._entries)

    @property
    def is_empty(self) -> bool:
        """
        Whether the registry is empty.
        """
        return self.size == 0

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        *,
        key: K,
        value: T,
    ) -> T:
        """
        Register an entry.

        Raises:
            RegistryError:
                If the key already exists or validation fails.
        """
        with self._lock:
            self._validate_registration(
                key=key,
                value=value,
            )

            if key in self._entries:
                raise RegistryError(
                    message=f"{key!r} is already registered.",
                    error_code="REGISTRY_DUPLICATE",
                )

            self._before_register(
                key=key,
                value=value,
            )

            self._entries[key] = value

            self._after_register(
                key=key,
                value=value,
            )

            return value

    def register_many(
        self,
        entries: Mapping[K, T],
    ) -> None:
        """
        Register multiple entries.
        """
        for key, value in entries.items():
            self.register(
                key=key,
                value=value,
            )

    def unregister(
        self,
        key: K,
    ) -> T:
        """
        Remove an entry.

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

            value = self._entries[key]

            self._before_unregister(
                key=key,
                value=value,
            )

            del self._entries[key]

            self._after_unregister(
                key=key,
                value=value,
            )

            return value

    def clear(self) -> None:
        """
        Remove all registered entries.
        """
        with self._lock:
            self._entries.clear()

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        key: K,
        default: T | None = None,
    ) -> T | None:
        """
        Retrieve an entry.
        """
        return self._entries.get(
            key,
            default,
        )

    def require(
        self,
        key: K,
    ) -> T:
        """
        Retrieve a required entry.

        Raises:
            RegistryError:
                If the entry does not exist.
        """
        value = self.get(key)

        if value is None:
            raise RegistryError(
                message=f"{key!r} is not registered.",
                error_code="REGISTRY_NOT_FOUND",
            )

        return value

    def exists(
        self,
        key: K,
    ) -> bool:
        """
        Determine whether an entry exists.
        """
        return key in self._entries

    # ------------------------------------------------------------------
    # Snapshots
    # ------------------------------------------------------------------

    def snapshot(
        self,
    ) -> Mapping[K, T]:
        """
        Return an immutable snapshot of the registry.
        """
        with self._lock:
            return MappingProxyType(
                dict(self._entries),
            )

    def metadata(
        self,
    ) -> Metadata:
        """
        Registry metadata.
        """
        return {
            "name": self.name,
            "size": self.size,
            "is_empty": self.is_empty,
        }

    # ------------------------------------------------------------------
    # Collection Views
    # ------------------------------------------------------------------

    def keys(
        self,
    ) -> Iterable[K]:
        """
        Registry keys.
        """
        return tuple(
            self._entries.keys(),
        )

    def values(
        self,
    ) -> Iterable[T]:
        """
        Registry values.
        """

        return tuple(
            self._entries.values(),
        )

    def all(
        self,
    ) -> Iterable[T]:
        """
        Return all registered values.
        """

        return self.values()

    def items(
        self,
    ) -> Iterable[tuple[K, T]]:
        """
        Registry items.
        """
        return tuple(
            self._entries.items(),
        )

    def copy(
        self,
    ) -> dict[K, T]:
        """
        Return a shallow copy of the registry.
        """
        with self._lock:
            return dict(
                self._entries,
            )

    # ------------------------------------------------------------------
    # Validation Hooks
    # ------------------------------------------------------------------

    def _validate_registration(
        self,
        *,
        key: K,
        value: T,
    ) -> None:
        """
        Validate a registration before insertion.
        """
        if value is None:
            raise RegistryError(
                message="Registry value cannot be None.",
                error_code="REGISTRY_INVALID_VALUE",
            )

    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    def _before_register(
        self,
        *,
        key: K,
        value: T,
    ) -> None:
        """
        Hook executed before registration.

        Subclasses may override.
        """

    def _after_register(
        self,
        *,
        key: K,
        value: T,
    ) -> None:
        """
        Hook executed after registration.

        Subclasses may override.
        """

    def _before_unregister(
        self,
        *,
        key: K,
        value: T,
    ) -> None:
        """
        Hook executed before unregistration.

        Subclasses may override.
        """

    def _after_unregister(
        self,
        *,
        key: K,
        value: T,
    ) -> None:
        """
        Hook executed after unregistration.

        Subclasses may override.
        """

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __contains__(
        self,
        key: object,
    ) -> bool:
        """
        Determine whether a key exists.
        """
        return key in self._entries

    def __getitem__(
        self,
        key: K,
    ) -> T:
        """
        Retrieve an entry.

        Raises:
            RegistryError:
                If the key does not exist.
        """
        return self.require(
            key,
        )

    def __iter__(
        self,
    ) -> Iterator[T]:
        """
        Iterate over registered values.
        """
        return iter(
            self._entries.values(),
        )

    def __len__(
        self,
    ) -> int:
        """
        Return the number of registered entries.
        """
        return self.size

    def __bool__(
        self,
    ) -> bool:
        """
        Whether the registry contains entries.
        """
        return not self.is_empty

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """
        return f"{type(self).__name__}(name={self.name!r}, size={self.size})"

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """
        return f"{self.name} ({self.size} registered)"


__all__ = [
    "BaseRegistry",
]

"""
DatavionOS Service Scope.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any


class ServiceScope:
    """
    Represents an isolated dependency
    injection scope.

    A scope owns scoped service instances
    created during a single unit of work,
    such as:

    - HTTP request
    - Background job
    - Workflow execution
    - Event processing
    - Scheduled task
    """

    def __init__(
        self,
        *,
        parent: ServiceScope | None = None,
    ) -> None:
        self._parent = parent
        self._instances: dict[
            type[Any],
            Any,
        ] = {}

        self._disposed = False

    @property
    def parent(
        self,
    ) -> ServiceScope | None:
        """
        Parent scope.
        """

        return self._parent

    @property
    def is_root(
        self,
    ) -> bool:
        """
        Indicates whether this is
        the root scope.
        """

        return self._parent is None

    @property
    def is_disposed(
        self,
    ) -> bool:
        """
        Indicates whether this scope
        has been disposed.
        """

        return self._disposed

    @property
    def count(
        self,
    ) -> int:
        """
        Number of scoped instances.
        """

        return len(
            self._instances,
        )

    def contains(
        self,
        service_type: type[Any],
    ) -> bool:
        """
        Determine whether a scoped
        instance exists.
        """

        return service_type in self._instances

    def get(
        self,
        service_type: type[Any],
    ) -> Any:
        """
        Retrieve a scoped instance.
        """

        return self._instances[service_type]

    def try_get(
        self,
        service_type: type[Any],
    ) -> Any | None:
        """
        Attempt to retrieve a scoped
        instance.
        """

        return self._instances.get(
            service_type,
        )

    def set(
        self,
        service_type: type[Any],
        instance: Any,
    ) -> None:
        """
        Store a scoped instance.
        """

        self._instances[service_type] = instance

    def remove(
        self,
        service_type: type[Any],
    ) -> None:
        """
        Remove a scoped instance.
        """

        self._instances.pop(
            service_type,
            None,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove every scoped instance.
        """

        self._instances.clear()

    def dispose(
        self,
    ) -> None:
        """
        Dispose the scope.

        Services implementing a dispose()
        method will be disposed in reverse
        registration order.
        """

        if self._disposed:
            return

        for instance in reversed(
            tuple(
                self._instances.values(),
            ),
        ):
            dispose = getattr(
                instance,
                "dispose",
                None,
            )

            if callable(
                dispose,
            ):
                dispose()

        self.clear()

        self._disposed = True

    def __contains__(
        self,
        service_type: type[Any],
    ) -> bool:
        return self.contains(
            service_type,
        )

    def __getitem__(
        self,
        service_type: type[Any],
    ) -> Any:
        return self.get(
            service_type,
        )

    def __iter__(
        self,
    ) -> Iterator[Any]:
        return iter(
            self._instances.values(),
        )

    def __len__(
        self,
    ) -> int:
        return self.count

    def __repr__(
        self,
    ) -> str:
        return f"ServiceScope(instances={self.count}, disposed={self.is_disposed})"


__all__ = [
    "ServiceScope",
]

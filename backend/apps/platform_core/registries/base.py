"""
Base registry implementation.
"""

from __future__ import annotations


class BaseRegistry[T]:
    """
    Base registry for platform resources.
    """

    def __init__(
        self,
    ) -> None:
        self._items: dict[str, T] = {}

    def register(
        self,
        key: str,
        item: T,
    ) -> None:
        """
        Register an item.
        """

        if key in self._items:
            raise ValueError(
                f"{key!r} is already registered.",
            )

        self._items[key] = item

    def unregister(
        self,
        key: str,
    ) -> None:
        """
        Remove an item.
        """

        self._items.pop(
            key,
            None,
        )

    def get(
        self,
        key: str,
    ) -> T:
        """
        Return a registered item.
        """

        return self._items[key]

    def all(
        self,
    ) -> list[T]:
        """
        Return all registered items.
        """

        return sorted(
            self._items.values(),
            key=lambda item: getattr(
                item,
                "order",
                0,
            ),
        )

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check whether an item exists.
        """

        return key in self._items

    def clear(
        self,
    ) -> None:
        """
        Remove every registered item.
        """

        self._items.clear()


__all__ = [
    "BaseRegistry",
]

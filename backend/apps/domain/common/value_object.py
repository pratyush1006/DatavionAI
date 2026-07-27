"""
Domain value object abstractions.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)


class ValueObject(
    ABC,
):
    """
    Base class for immutable value objects.
    """

    @abstractmethod
    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        """
        Return the components that define equality.
        """

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare value objects by value.
        """
        if not isinstance(
            other,
            ValueObject,
        ):
            return False

        return (
            type(self) is type(other)
            and self._equality_components() == other._equality_components()
        )

    def __hash__(
        self,
    ) -> int:
        """
        Compute hash from equality components.
        """
        return hash(
            (
                type(self),
                self._equality_components(),
            ),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Debug representation.
        """
        values = ", ".join(repr(component) for component in self._equality_components())

        return f"{type(self).__name__}({values})"

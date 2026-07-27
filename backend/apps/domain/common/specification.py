"""
Domain specification abstractions.
"""

from __future__ import annotations

from typing import (
    Generic,
    Protocol,
    TypeVar,
    runtime_checkable,
)

T = TypeVar("T")


@runtime_checkable
class Specification(
    Protocol,
    Generic[T],
):
    """
    Domain specification contract.
    """

    def is_satisfied_by(
        self,
        candidate: T,
    ) -> bool:
        """
        Determine whether the candidate satisfies
        the specification.
        """


class AndSpecification(
    Generic[T],
):
    """
    Logical AND specification.
    """

    def __init__(
        self,
        left: Specification[T],
        right: Specification[T],
    ) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(
        self,
        candidate: T,
    ) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(
            candidate
        )


class OrSpecification(
    Generic[T],
):
    """
    Logical OR specification.
    """

    def __init__(
        self,
        left: Specification[T],
        right: Specification[T],
    ) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(
        self,
        candidate: T,
    ) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(
            candidate
        )


class NotSpecification(
    Generic[T],
):
    """
    Logical NOT specification.
    """

    def __init__(
        self,
        specification: Specification[T],
    ) -> None:
        self._specification = specification

    def is_satisfied_by(
        self,
        candidate: T,
    ) -> bool:
        return not self._specification.is_satisfied_by(
            candidate,
        )


__all__ = [
    "Specification",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
]

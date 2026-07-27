"""
Query specification contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Generic,
    Protocol,
    TypeVar,
    runtime_checkable,
)

TEntity = TypeVar("TEntity")


@dataclass(
    frozen=True,
    slots=True,
)
class Sort:
    """
    Immutable sort definition.
    """

    field: str

    descending: bool = False


@dataclass(
    frozen=True,
    slots=True,
)
class Pagination:
    """
    Immutable pagination definition.
    """

    offset: int = 0

    limit: int | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class Specification(
    Generic[TEntity],
):
    """
    Immutable query specification.
    """

    filters: dict[str, Any] = field(
        default_factory=dict,
    )

    sort: tuple[Sort, ...] = ()

    pagination: Pagination | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class SpecificationEvaluator(
    Protocol,
    Generic[TEntity],
):
    """
    Evaluates query specifications.
    """

    async def evaluate(
        self,
        specification: Specification[TEntity],
    ) -> tuple[TEntity, ...]:
        """
        Evaluate a specification.
        """


__all__ = [
    "Pagination",
    "Sort",
    "Specification",
    "SpecificationEvaluator",
]

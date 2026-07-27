"""
Repository contracts.
"""

from __future__ import annotations

from typing import (
    Generic,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from apps.datavionos.persistence.specification import (
    Specification,
)

TEntity = TypeVar("TEntity")

TIdentifier = TypeVar("TIdentifier")


@runtime_checkable
class Repository(
    Protocol,
    Generic[TEntity, TIdentifier],
):
    """
    Generic repository contract.
    """

    async def get(
        self,
        identifier: TIdentifier,
    ) -> TEntity | None:
        """
        Return an entity by its identifier.
        """

    async def add(
        self,
        entity: TEntity,
    ) -> None:
        """
        Add a new entity.
        """

    async def update(
        self,
        entity: TEntity,
    ) -> None:
        """
        Update an existing entity.
        """

    async def remove(
        self,
        entity: TEntity,
    ) -> None:
        """
        Remove an entity.
        """

    async def exists(
        self,
        identifier: TIdentifier,
    ) -> bool:
        """
        Determine whether an entity exists.
        """

    async def list(
        self,
        specification: Specification[TEntity] | None = None,
    ) -> tuple[TEntity, ...]:
        """
        Return entities matching a specification.
        """

    async def count(
        self,
        specification: Specification[TEntity] | None = None,
    ) -> int:
        """
        Return the number of matching entities.
        """


__all__ = [
    "Repository",
]

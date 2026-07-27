"""
Domain repository contracts.
"""

from __future__ import annotations

from typing import (
    Generic,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from apps.domain.common.aggregate import (
    AggregateRoot,
)

TAggregate = TypeVar(
    "TAggregate",
    bound=AggregateRoot,
)

TIdentity = TypeVar("TIdentity")


@runtime_checkable
class Repository(
    Protocol,
    Generic[
        TAggregate,
        TIdentity,
    ],
):
    """
    Repository contract for aggregate roots.
    """

    async def get_by_id(
        self,
        identity: TIdentity,
    ) -> TAggregate | None:
        """
        Retrieve an aggregate by its identity.
        """

    async def exists(
        self,
        identity: TIdentity,
    ) -> bool:
        """
        Determine whether an aggregate exists.
        """

    async def add(
        self,
        aggregate: TAggregate,
    ) -> None:
        """
        Add a new aggregate.
        """

    async def update(
        self,
        aggregate: TAggregate,
    ) -> None:
        """
        Persist aggregate changes.
        """

    async def remove(
        self,
        aggregate: TAggregate,
    ) -> None:
        """
        Remove an aggregate.
        """

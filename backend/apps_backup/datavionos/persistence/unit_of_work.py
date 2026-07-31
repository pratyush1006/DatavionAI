"""
Unit of Work contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.persistence.repository import (
    Repository,
)
from apps.datavionos.persistence.transaction import (
    Transaction,
)


@runtime_checkable
class UnitOfWork(
    Protocol,
):
    """
    Coordinates repositories and transactions.
    """

    @property
    def transaction(
        self,
    ) -> Transaction:
        """
        Return the active transaction.
        """

    def repository(
        self,
        entity_type: type,
    ) -> Repository:
        """
        Return the repository for an entity type.
        """

    async def commit(
        self,
    ) -> None:
        """
        Commit all pending changes.
        """

    async def rollback(
        self,
    ) -> None:
        """
        Roll back all pending changes.
        """

    async def __aenter__(
        self,
    ) -> UnitOfWork:
        """
        Enter the unit of work context.
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        """
        Exit the unit of work context.
        """


__all__ = [
    "UnitOfWork",
]

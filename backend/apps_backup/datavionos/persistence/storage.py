"""
Storage provider contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.persistence.transaction import (
    Transaction,
)
from apps.datavionos.persistence.unit_of_work import (
    UnitOfWork,
)


@runtime_checkable
class StorageProvider(
    Protocol,
):
    """
    Provides access to a persistence backend.
    """

    async def connect(
        self,
    ) -> None:
        """
        Connect to the storage backend.
        """

    async def disconnect(
        self,
    ) -> None:
        """
        Disconnect from the storage backend.
        """

    async def is_connected(
        self,
    ) -> bool:
        """
        Determine whether the storage backend is connected.
        """

    async def create_transaction(
        self,
    ) -> Transaction:
        """
        Create a new transaction.
        """

    async def create_unit_of_work(
        self,
    ) -> UnitOfWork:
        """
        Create a new unit of work.
        """


__all__ = [
    "StorageProvider",
]

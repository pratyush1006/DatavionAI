"""
Transaction contracts.
"""

from __future__ import annotations

from enum import StrEnum
from typing import (
    Protocol,
    runtime_checkable,
)


class TransactionStatus(
    StrEnum,
):
    """
    Transaction status.
    """

    ACTIVE = "active"

    COMMITTED = "committed"

    ROLLED_BACK = "rolled_back"


@runtime_checkable
class Transaction(
    Protocol,
):
    """
    Transaction contract.
    """

    @property
    def status(
        self,
    ) -> TransactionStatus:
        """
        Return the current transaction status.
        """

    async def commit(
        self,
    ) -> None:
        """
        Commit the transaction.
        """

    async def rollback(
        self,
    ) -> None:
        """
        Roll back the transaction.
        """

    async def close(
        self,
    ) -> None:
        """
        Release transaction resources.
        """

    async def __aenter__(
        self,
    ) -> Transaction:
        """
        Enter the transaction context.
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        """
        Exit the transaction context.
        """


__all__ = [
    "Transaction",
    "TransactionStatus",
]

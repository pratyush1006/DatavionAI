"""
DatavionAI Service Transactions.

Reusable transaction helpers for enterprise services.

Design Principles
-----------------
- Framework agnostic
- Atomic by default
- Nesting friendly
- Extensible
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from django.db import transaction

F = TypeVar(
    "F",
    bound=Callable[..., Any],
)


class TransactionService:
    """
    Shared transaction helpers.
    """

    @staticmethod
    def atomic() -> Callable[[F], F]:
        """
        Execute a function inside a database transaction.
        """

        return transaction.atomic

    @staticmethod
    def on_commit(
        callback: Callable[[], None],
    ) -> None:
        """
        Register a callback executed after commit.
        """

        transaction.on_commit(callback)

    @staticmethod
    def non_atomic(
        func: F,
    ) -> F:
        """
        Execute outside an atomic transaction.
        """

        @wraps(func)
        def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            with transaction.non_atomic_requests(using=None):
                return func(
                    *args,
                    **kwargs,
                )

        return wrapper  # type: ignore[return-value]

    @staticmethod
    def savepoint() -> str:
        """
        Create a database savepoint.
        """

        return transaction.savepoint()

    @staticmethod
    def savepoint_commit(
        sid: str,
    ) -> None:
        """
        Commit a savepoint.
        """

        transaction.savepoint_commit(sid)

    @staticmethod
    def savepoint_rollback(
        sid: str,
    ) -> None:
        """
        Roll back to a savepoint.
        """

        transaction.savepoint_rollback(sid)

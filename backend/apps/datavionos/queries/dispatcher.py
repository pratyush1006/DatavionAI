"""
DatavionOS Query Dispatcher Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from apps.datavionos.queries.query import (
    Query,
)

TQuery = TypeVar(
    "TQuery",
    bound=Query,
)

TResult = TypeVar(
    "TResult",
)


class QueryDispatcher(
    ABC,
    Generic[
        TQuery,
        TResult,
    ],
):
    """
    Base contract for all query
    dispatchers.

    A dispatcher is responsible for
    locating the appropriate handler and
    returning the query result.
    """

    @abstractmethod
    def dispatch(
        self,
        query: TQuery,
    ) -> TResult:
        """
        Dispatch a query.
        """

    def dispatch_many(
        self,
        *queries: TQuery,
    ) -> tuple[TResult, ...]:
        """
        Dispatch multiple queries.
        """

        return tuple(
            self.dispatch(
                query,
            )
            for query in queries
        )

    def __call__(
        self,
        query: TQuery,
    ) -> TResult:
        """
        Invoke the dispatcher.
        """

        return self.dispatch(
            query,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.__class__.__name__}()"


__all__ = [
    "QueryDispatcher",
]

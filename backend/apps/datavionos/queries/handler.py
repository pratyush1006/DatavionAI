"""
DatavionOS Query Handler Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

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


class QueryHandler[TQuery: Query, TResult](
    ABC,
):
    """
    Base class for all query handlers.

    Query handlers are responsible for
    retrieving data without modifying
    application state.
    """

    @property
    @abstractmethod
    def query_type(
        self,
    ) -> type[TQuery]:
        """
        Supported query type.
        """

    @property
    def handler_name(
        self,
    ) -> str:
        """
        Handler name.
        """

        return self.__class__.__qualname__

    @abstractmethod
    def handle(
        self,
        query: TQuery,
    ) -> TResult:
        """
        Execute the query.
        """

    def can_handle(
        self,
        query: Query,
    ) -> bool:
        """
        Determine whether this handler
        supports the supplied query.
        """

        return isinstance(
            query,
            self.query_type,
        )

    def __call__(
        self,
        query: TQuery,
    ) -> TResult:
        """
        Invoke the handler.
        """

        return self.handle(
            query,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.handler_name}(query_type={self.query_type.__qualname__})"


__all__ = [
    "QueryHandler",
]

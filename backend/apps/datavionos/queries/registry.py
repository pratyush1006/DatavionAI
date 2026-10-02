"""
DatavionOS Query Handler Registry.
"""

from __future__ import annotations

from typing import Any

from apps.datavionos.queries.handler import (
    QueryHandler,
)
from apps.datavionos.queries.query import (
    Query,
)


class QueryRegistry:
    """
    Registry for query handlers.

    Maintains a one-to-one mapping between
    query types and their handlers.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._handlers: dict[
            type[Query],
            QueryHandler[Any, Any],
        ] = {}

    @property
    def handler_count(
        self,
    ) -> int:
        """
        Number of registered handlers.
        """

        return len(
            self._handlers,
        )

    def register(
        self,
        handler: QueryHandler[Any, Any],
    ) -> None:
        """
        Register a query handler.
        """

        query_type = handler.query_type

        if query_type in self._handlers:
            raise ValueError(
                (f"Handler already registered for query {query_type.__qualname__}."),
            )

        self._handlers[query_type] = handler

    def unregister(
        self,
        query_type: type[Query],
    ) -> None:
        """
        Remove a handler registration.
        """

        self._handlers.pop(
            query_type,
            None,
        )

    def contains(
        self,
        query_type: type[Query],
    ) -> bool:
        """
        Determine whether a handler
        exists for a query.
        """

        return query_type in self._handlers

    def get(
        self,
        query_type: type[Query],
    ) -> QueryHandler[Any, Any]:
        """
        Retrieve a handler.
        """

        return self._handlers[query_type]

    def try_get(
        self,
        query_type: type[Query],
    ) -> QueryHandler[Any, Any] | None:
        """
        Retrieve a handler if registered.
        """

        return self._handlers.get(
            query_type,
        )

    @property
    def query_types(
        self,
    ) -> tuple[type[Query], ...]:
        """
        Registered query types.
        """

        return tuple(
            self._handlers.keys(),
        )

    @property
    def handlers(
        self,
    ) -> tuple[
        QueryHandler[Any, Any],
        ...,
    ]:
        """
        Registered handlers.
        """

        return tuple(
            self._handlers.values(),
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all handler registrations.
        """

        self._handlers.clear()

    def __contains__(
        self,
        query_type: type[Query],
    ) -> bool:
        """
        Support the 'in' operator.
        """

        return self.contains(
            query_type,
        )

    def __len__(
        self,
    ) -> int:
        """
        Number of handlers.
        """

        return self.handler_count

    def __iter__(
        self,
    ):
        """
        Iterate over registered handlers.
        """

        return iter(
            self._handlers.values(),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.__class__.__name__}(handlers={self.handler_count})"


__all__ = [
    "QueryRegistry",
]

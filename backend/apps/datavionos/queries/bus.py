"""
DatavionOS Query Bus.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from apps.datavionos.queries.dispatcher import (
    QueryDispatcher,
)
from apps.datavionos.queries.handler import (
    QueryHandler,
)
from apps.datavionos.queries.middleware import (
    QueryMiddleware,
)
from apps.datavionos.queries.query import (
    Query,
)
from apps.datavionos.queries.registry import (
    QueryRegistry,
)


class QueryBus(QueryDispatcher):
    """
    Default in-process query bus.

    Responsible for locating the appropriate
    handler and executing the middleware pipeline.
    """

    def __init__(
        self,
        registry: QueryRegistry,
    ) -> None:
        """
        Initialize query bus.
        """

        self._registry = registry

        self._middleware: list[Any] = []

    @property
    def registry(
        self,
    ) -> QueryRegistry:
        """
        Query registry.
        """

        return self._registry

    @property
    def middleware_count(
        self,
    ) -> int:
        """
        Number of registered middleware.
        """

        return len(
            self._middleware,
        )

    def register(
        self,
        handler: QueryHandler[Any, Any],
    ) -> None:
        """
        Register a query handler.
        """

        self._registry.register(
            handler,
        )

    def add_middleware(
        self,
        middleware: QueryMiddleware,
    ) -> None:
        """
        Register query middleware.
        """

        self._middleware.append(
            middleware,
        )

    def remove_middleware(
        self,
        middleware: Any,
    ) -> None:
        """
        Remove middleware if registered.
        """

        if middleware in self._middleware:
            self._middleware.remove(
                middleware,
            )

    def clear_middleware(
        self,
    ) -> None:
        """
        Remove all registered middleware.
        """

        self._middleware.clear()

    def has_middleware(
        self,
        middleware: Any,
    ) -> bool:
        """
        Determine whether middleware is registered.
        """

        return middleware in self._middleware

    def _build_pipeline(
        self,
        query: Query,
        handler: QueryHandler[Any, Any],
    ) -> Any:
        """
        Build the middleware execution pipeline.
        """

        def terminal() -> Any:
            return handler.handle(
                query,
            )

        next_callable: Callable[[], Any] = terminal

        for middleware in reversed(
            self._middleware,
        ):
            current = middleware

            def make_next(
                inner: QueryMiddleware,
                outer: Callable[[], Any],
            ) -> Callable[[], Any]:
                def step() -> Any:
                    return inner(
                        query,
                        outer,
                    )

                return step

            next_callable = make_next(
                current,
                next_callable,
            )

        return next_callable()

    def dispatch(
        self,
        query: Query,
    ) -> Any:
        """
        Dispatch a query through the pipeline.
        """

        handler = self._registry.get(
            type(query),
        )

        return self._build_pipeline(
            query,
            handler,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"handlers={self.registry.handler_count}, "
            f"middleware={self.middleware_count})"
        )


__all__ = [
    "QueryBus",
]

"""
DatavionOS Query Middleware Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from apps.datavionos.queries.query import (
    Query,
)


class QueryMiddleware(ABC):
    """
    Base middleware for the query pipeline.

    Middleware participates in query
    execution before and after the handler
    executes.
    """

    @property
    def middleware_name(
        self,
    ) -> str:
        """
        Middleware name.
        """

        return self.__class__.__name__

    @property
    def priority(
        self,
    ) -> int:
        """
        Execution priority.

        Lower values execute earlier.
        """

        return 0

    def before_dispatch(
        self,
        query: Query,
    ) -> None:
        """
        Executed before the query enters
        the pipeline.
        """

    @abstractmethod
    def invoke(
        self,
        query: Query,
        next_callable: Callable[[], Any],
    ) -> Any:
        """
        Execute middleware.

        Must invoke next_callable() to
        continue pipeline execution.
        """

    def after_dispatch(
        self,
        query: Query,
        result: Any,
    ) -> Any:
        """
        Executed after successful query
        execution.
        """

        return result

    def on_success(
        self,
        query: Query,
        result: Any,
    ) -> None:
        """
        Invoked after successful query
        execution.
        """

    def on_failure(
        self,
        query: Query,
        exception: Exception,
    ) -> None:
        """
        Invoked when query execution
        fails.
        """

    def __call__(
        self,
        query: Query,
        next_callable: Callable[[], Any],
    ) -> Any:
        """
        Execute the middleware lifecycle.
        """

        self.before_dispatch(
            query,
        )

        try:
            result = self.invoke(
                query,
                next_callable,
            )

            result = self.after_dispatch(
                query,
                result,
            )

            self.on_success(
                query,
                result,
            )

            return result

        except Exception as exc:
            self.on_failure(
                query,
                exc,
            )
            raise

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.middleware_name}(priority={self.priority})"


__all__ = [
    "QueryMiddleware",
]

"""
DatavionOS Query Exceptions.
"""

from __future__ import annotations

from apps.datavionos.queries.query import (
    Query,
)


class QueryException(Exception):
    """
    Base exception for all query
    pipeline failures.
    """

    def __init__(
        self,
        message: str,
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            message,
        )

        self.query_name = query_name


class QueryHandlerNotFoundException(
    QueryException,
):
    """
    Raised when no handler is registered
    for a query.
    """

    def __init__(
        self,
        query_type: type[Query],
    ) -> None:
        super().__init__(
            (f"No query handler is registered for {query_type.__qualname__}."),
            query_name=query_type.__qualname__,
        )


class DuplicateQueryHandlerException(
    QueryException,
):
    """
    Raised when multiple handlers are
    registered for the same query.
    """

    def __init__(
        self,
        query_type: type[Query],
    ) -> None:
        super().__init__(
            (f"A handler has already been registered for {query_type.__qualname__}."),
            query_name=query_type.__qualname__,
        )


class QueryValidationException(
    QueryException,
):
    """
    Raised when query validation fails.
    """

    def __init__(
        self,
        message: str,
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            message,
            query_name=query_name,
        )


class QueryAuthorizationException(
    QueryException,
):
    """
    Raised when authorization fails.
    """

    def __init__(
        self,
        message: str = ("Query authorization failed."),
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            message,
            query_name=query_name,
        )


class QueryExecutionException(
    QueryException,
):
    """
    Raised when query execution fails.
    """

    def __init__(
        self,
        message: str,
        *,
        query_name: str = "",
        inner_exception: Exception | None = None,
    ) -> None:
        super().__init__(
            message,
            query_name=query_name,
        )

        self.inner_exception = inner_exception


class QueryTimeoutException(
    QueryException,
):
    """
    Raised when query execution exceeds
    the configured timeout.
    """

    def __init__(
        self,
        timeout_seconds: float,
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            (f"Query execution exceeded {timeout_seconds:.2f} seconds."),
            query_name=query_name,
        )

        self.timeout_seconds = timeout_seconds


class QueryCancelledException(
    QueryException,
):
    """
    Raised when query execution
    is cancelled.
    """

    def __init__(
        self,
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            "Query execution was cancelled.",
            query_name=query_name,
        )


class QueryCacheException(
    QueryException,
):
    """
    Raised when cache operations fail.
    """

    def __init__(
        self,
        message: str,
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            message,
            query_name=query_name,
        )


class QueryReadSourceException(
    QueryException,
):
    """
    Raised when an invalid read source
    is selected.
    """

    def __init__(
        self,
        read_source: str,
        *,
        query_name: str = "",
    ) -> None:
        super().__init__(
            (f"Invalid read source {read_source!r}."),
            query_name=query_name,
        )

        self.read_source = read_source


class QueryMiddlewareException(
    QueryException,
):
    """
    Raised when query middleware fails.
    """

    def __init__(
        self,
        middleware_name: str,
        *,
        query_name: str = "",
        inner_exception: Exception | None = None,
    ) -> None:
        super().__init__(
            (f"Middleware {middleware_name} failed."),
            query_name=query_name,
        )

        self.middleware_name = middleware_name

        self.inner_exception = inner_exception


__all__ = [
    "QueryException",
    "QueryHandlerNotFoundException",
    "DuplicateQueryHandlerException",
    "QueryValidationException",
    "QueryAuthorizationException",
    "QueryExecutionException",
    "QueryTimeoutException",
    "QueryCancelledException",
    "QueryCacheException",
    "QueryReadSourceException",
    "QueryMiddlewareException",
]

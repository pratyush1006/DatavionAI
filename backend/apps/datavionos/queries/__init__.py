"""
DatavionOS Query Processing Framework.

This package provides the foundational CQRS query
infrastructure used throughout DatavionOS.

Public API:
    - Query
    - QueryHandler
    - QueryDispatcher
    - QueryRegistry
    - QueryBus
    - QueryMiddleware
    - QueryContext
    - QueryResult

Exceptions:
    - QueryException
    - QueryHandlerNotFoundException
    - DuplicateQueryHandlerException
    - QueryValidationException
    - QueryAuthorizationException
    - QueryExecutionException
    - QueryTimeoutException
    - QueryCancelledException
    - QueryCacheException
    - QueryReadSourceException
    - QueryMiddlewareException
"""

from __future__ import annotations

from apps.datavionos.queries.bus import (
    QueryBus,
)
from apps.datavionos.queries.context import (
    QueryContext,
)
from apps.datavionos.queries.dispatcher import (
    QueryDispatcher,
)
from apps.datavionos.queries.exceptions import (
    DuplicateQueryHandlerException,
    QueryAuthorizationException,
    QueryCacheException,
    QueryCancelledException,
    QueryException,
    QueryExecutionException,
    QueryHandlerNotFoundException,
    QueryMiddlewareException,
    QueryReadSourceException,
    QueryTimeoutException,
    QueryValidationException,
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
from apps.datavionos.queries.result import (
    QueryResult,
)

__all__ = [
    # Core Contracts
    "Query",
    "QueryHandler",
    "QueryDispatcher",
    "QueryRegistry",
    "QueryBus",
    "QueryMiddleware",
    "QueryContext",
    "QueryResult",
    # Exceptions
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

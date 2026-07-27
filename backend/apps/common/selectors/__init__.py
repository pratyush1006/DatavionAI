"""
DatavionOS Selector Framework.

Enterprise selector framework for reusable
read operations throughout the platform.

Provides:

- Query selectors
- Filtering
- Searching
- Ordering
- Offset pagination
- Cursor pagination
- Selector utilities
"""

from __future__ import annotations

# ============================================================================
# Selector Modules
# ============================================================================
from . import (
    base,
    cursor,
    filters,
    mixins,
    ordering,
    pagination,
    registry,
    search,
    utils,
)

# ============================================================================
# Public Classes
# ============================================================================
from .base import (
    BaseSelector,
)
from .cursor import (
    CursorPagination,
    CursorPaginationResult,
)
from .pagination import (
    Pagination,
    PaginationResult,
)

__all__: tuple[str, ...] = (
    # Modules
    "base",
    "filters",
    "mixins",
    "ordering",
    "pagination",
    "cursor",
    "registry",
    "search",
    "utils",
    # Base Selector
    "BaseSelector",
    # Offset Pagination
    "Pagination",
    "PaginationResult",
    # Cursor Pagination
    "CursorPagination",
    "CursorPaginationResult",
)

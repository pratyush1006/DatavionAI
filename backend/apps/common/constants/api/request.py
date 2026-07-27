"""
DatavionAI API Request Constants.

Centralized request parameter definitions shared across the DatavionAI
platform.

This module defines immutable query parameter names, filtering constants,
search modes, ordering options, sparse field selection, and bulk operation
identifiers.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- No response constants
- No routing constants
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Standard Query Parameters
###############################################################################

QUERY_PAGE: Final[str] = "page"

QUERY_PAGE_SIZE: Final[str] = "page_size"

QUERY_LIMIT: Final[str] = "limit"

QUERY_OFFSET: Final[str] = "offset"

QUERY_CURSOR: Final[str] = "cursor"

QUERY_SEARCH: Final[str] = "search"

QUERY_QUERY: Final[str] = "query"

QUERY_ORDERING: Final[str] = "ordering"

QUERY_SORT: Final[str] = "sort"

QUERY_DIRECTION: Final[str] = "direction"

QUERY_FIELDS: Final[str] = "fields"

QUERY_INCLUDE: Final[str] = "include"

QUERY_EXCLUDE: Final[str] = "exclude"

QUERY_EXPAND: Final[str] = "expand"

QUERY_FORMAT: Final[str] = "format"

QUERY_VIEW: Final[str] = "view"

QUERY_LANGUAGE: Final[str] = "language"

QUERY_LOCALE: Final[str] = "locale"

QUERY_TIMEZONE: Final[str] = "timezone"

###############################################################################
# Generic Filters
###############################################################################

QUERY_FILTER: Final[str] = "filter"

QUERY_FILTERS: Final[str] = "filters"

QUERY_STATUS: Final[str] = "status"

QUERY_STATE: Final[str] = "state"

QUERY_TYPE: Final[str] = "type"

QUERY_CATEGORY: Final[str] = "category"

QUERY_PRIORITY: Final[str] = "priority"

QUERY_LABEL: Final[str] = "label"

QUERY_TAG: Final[str] = "tag"

QUERY_OWNER: Final[str] = "owner"

QUERY_ACTIVE: Final[str] = "active"

QUERY_ENABLED: Final[str] = "enabled"

QUERY_ARCHIVED: Final[str] = "archived"

QUERY_DELETED: Final[str] = "deleted"

###############################################################################
# Identifier Filters
###############################################################################

QUERY_ID: Final[str] = "id"

QUERY_UUID: Final[str] = "uuid"

QUERY_SLUG: Final[str] = "slug"

QUERY_CODE: Final[str] = "code"

QUERY_NAME: Final[str] = "name"

QUERY_REFERENCE: Final[str] = "reference"

QUERY_EXTERNAL_ID: Final[str] = "external_id"

###############################################################################
# Date Filters
###############################################################################

QUERY_DATE: Final[str] = "date"

QUERY_FROM: Final[str] = "from"

QUERY_TO: Final[str] = "to"

QUERY_START_DATE: Final[str] = "start_date"

QUERY_END_DATE: Final[str] = "end_date"

QUERY_CREATED_AFTER: Final[str] = "created_after"

QUERY_CREATED_BEFORE: Final[str] = "created_before"

QUERY_UPDATED_AFTER: Final[str] = "updated_after"

QUERY_UPDATED_BEFORE: Final[str] = "updated_before"

###############################################################################
# Search Modes
###############################################################################


class SearchMode(StrEnum):
    """
    Supported search modes.
    """

    EXACT = "exact"

    CONTAINS = "contains"

    STARTS_WITH = "startswith"

    ENDS_WITH = "endswith"

    FULL_TEXT = "fulltext"

    FUZZY = "fuzzy"


SUPPORTED_SEARCH_MODES: Final[tuple[str, ...]] = (
    SearchMode.EXACT.value,
    SearchMode.CONTAINS.value,
    SearchMode.STARTS_WITH.value,
    SearchMode.ENDS_WITH.value,
    SearchMode.FULL_TEXT.value,
    SearchMode.FUZZY.value,
)

###############################################################################
# Sorting
###############################################################################

ORDER_ASC: Final[str] = "asc"

ORDER_DESC: Final[str] = "desc"

DEFAULT_SORT_DIRECTION: Final[str] = ORDER_DESC

DEFAULT_ORDERING_FIELD: Final[str] = "created_at"

###############################################################################
# Sparse Fieldsets
###############################################################################

FIELDS_ALL: Final[str] = "*"

FIELDS_DEFAULT: Final[str] = "default"

FIELDS_MINIMAL: Final[str] = "minimal"

FIELDS_DETAILED: Final[str] = "detailed"

###############################################################################
# Relationship Expansion
###############################################################################

EXPAND_ALL: Final[str] = "*"

EXPAND_NONE: Final[str] = "none"

EXPAND_PARENT: Final[str] = "parent"

EXPAND_CHILDREN: Final[str] = "children"

###############################################################################
# Include / Exclude
###############################################################################

INCLUDE_ALL: Final[str] = "*"

EXCLUDE_NONE: Final[str] = "none"

###############################################################################
# Bulk Operations
###############################################################################


class BulkOperation(StrEnum):
    """
    Supported bulk operations.
    """

    CREATE = "bulk_create"

    UPDATE = "bulk_update"

    DELETE = "bulk_delete"

    RESTORE = "bulk_restore"

    IMPORT = "bulk_import"

    EXPORT = "bulk_export"


SUPPORTED_BULK_OPERATIONS: Final[tuple[str, ...]] = (
    BulkOperation.CREATE.value,
    BulkOperation.UPDATE.value,
    BulkOperation.DELETE.value,
    BulkOperation.RESTORE.value,
    BulkOperation.IMPORT.value,
    BulkOperation.EXPORT.value,
)

###############################################################################
# Reserved Query Parameters
###############################################################################

RESERVED_QUERY_PARAMETERS: Final[frozenset[str]] = frozenset(
    {
        QUERY_PAGE,
        QUERY_PAGE_SIZE,
        QUERY_LIMIT,
        QUERY_OFFSET,
        QUERY_CURSOR,
        QUERY_SEARCH,
        QUERY_ORDERING,
        QUERY_SORT,
        QUERY_FIELDS,
        QUERY_INCLUDE,
        QUERY_EXCLUDE,
        QUERY_EXPAND,
        QUERY_FORMAT,
        QUERY_VIEW,
        QUERY_LANGUAGE,
        QUERY_LOCALE,
        QUERY_TIMEZONE,
    }
)

###############################################################################
# Query Parameter Groups
###############################################################################

PAGINATION_PARAMETERS: Final[frozenset[str]] = frozenset(
    {
        QUERY_PAGE,
        QUERY_PAGE_SIZE,
        QUERY_LIMIT,
        QUERY_OFFSET,
        QUERY_CURSOR,
    }
)

SEARCH_PARAMETERS: Final[frozenset[str]] = frozenset(
    {
        QUERY_SEARCH,
        QUERY_QUERY,
        QUERY_FILTER,
        QUERY_FILTERS,
        QUERY_SORT,
        QUERY_ORDERING,
    }
)

LOCALIZATION_PARAMETERS: Final[frozenset[str]] = frozenset(
    {
        QUERY_LANGUAGE,
        QUERY_LOCALE,
        QUERY_TIMEZONE,
    }
)

DATE_FILTER_PARAMETERS: Final[frozenset[str]] = frozenset(
    {
        QUERY_DATE,
        QUERY_FROM,
        QUERY_TO,
        QUERY_START_DATE,
        QUERY_END_DATE,
        QUERY_CREATED_AFTER,
        QUERY_CREATED_BEFORE,
        QUERY_UPDATED_AFTER,
        QUERY_UPDATED_BEFORE,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "SearchMode",
    "BulkOperation",
)

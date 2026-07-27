"""
DatavionOS Selector Pagination.

Framework-agnostic pagination utilities.

Supports:

- Page pagination
- Cursor pagination
- Large dataset traversal
- Immutable results
- Type safety
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from django.db.models import Model, QuerySet

ModelType = TypeVar(
    "ModelType",
    bound=Model,
)


# ============================================================================
# Offset Pagination
# ============================================================================


@dataclass(
    frozen=True,
    slots=True,
)
class PaginationResult(
    Generic[ModelType],
):
    """
    Offset pagination result.
    """

    queryset: QuerySet[ModelType]

    page: int

    page_size: int

    offset: int

    limit: int

    total_records: int

    total_pages: int

    has_next: bool

    has_previous: bool


class Pagination:
    """
    Standard page pagination.
    """

    DEFAULT_PAGE = 1

    DEFAULT_PAGE_SIZE = 25

    MAX_PAGE_SIZE = 100

    @classmethod
    def paginate(
        cls,
        queryset: QuerySet[ModelType],
        *,
        page: int = DEFAULT_PAGE,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginationResult[ModelType]:

        page = max(
            cls.DEFAULT_PAGE,
            page,
        )

        page_size = min(
            max(
                1,
                page_size,
            ),
            cls.MAX_PAGE_SIZE,
        )

        total_records = queryset.count()

        total_pages = (
            ceil(
                total_records / page_size,
            )
            if total_records
            else 0
        )

        offset = (page - 1) * page_size

        return PaginationResult(
            queryset=queryset[offset : offset + page_size],
            page=page,
            page_size=page_size,
            offset=offset,
            limit=page_size,
            total_records=total_records,
            total_pages=total_pages,
            has_next=(page < total_pages),
            has_previous=(page > 1),
        )


# ============================================================================
# Cursor Pagination
# ============================================================================


@dataclass(
    frozen=True,
    slots=True,
)
class CursorPaginationResult(
    Generic[ModelType],
):
    """
    Cursor pagination result.

    Designed for:

    - Patient timelines
    - Audit streams
    - Clinical observations
    - Event feeds
    """

    queryset: QuerySet[ModelType]

    next_cursor: str | None

    has_next: bool


class CursorPagination:
    """
    Cursor based pagination.

    Uses stable ordering.

    Recommended ordering:

    - created_at
    - uuid
    - id
    """

    DEFAULT_PAGE_SIZE = 50

    MAX_PAGE_SIZE = 200

    @staticmethod
    def encode_cursor(
        value: dict[str, object],
    ) -> str:
        """
        Encode cursor payload.
        """

        raw = json.dumps(
            value,
            separators=(
                ",",
                ":",
            ),
        )

        return base64.urlsafe_b64encode(
            raw.encode(),
        ).decode()

    @staticmethod
    def decode_cursor(
        cursor: str,
    ) -> dict[str, object]:
        """
        Decode cursor payload.
        """

        decoded = base64.urlsafe_b64decode(
            cursor.encode(),
        )

        return json.loads(
            decoded.decode(),
        )

    @classmethod
    def paginate(
        cls,
        queryset: QuerySet[ModelType],
        *,
        cursor: str | None = None,
        page_size: int = DEFAULT_PAGE_SIZE,
        ordering_field: str = "id",
    ) -> CursorPaginationResult[ModelType]:
        """
        Apply cursor pagination.
        """

        page_size = min(
            max(
                1,
                page_size,
            ),
            cls.MAX_PAGE_SIZE,
        )

        if cursor:
            payload = cls.decode_cursor(
                cursor,
            )

            last_value = payload["value"]

            queryset = queryset.filter(
                **{
                    f"{ordering_field}__gt": last_value,
                },
            )

        queryset = queryset.order_by(
            ordering_field,
        )

        results = list(queryset[: page_size + 1])

        has_next = len(results) > page_size

        items = results[:page_size]

        next_cursor = None

        if has_next:
            next_cursor = cls.encode_cursor(
                {
                    "value": getattr(
                        items[-1],
                        ordering_field,
                    ),
                }
            )

        return CursorPaginationResult(
            queryset=queryset.model.objects.filter(pk__in=[item.pk for item in items]),
            next_cursor=next_cursor,
            has_next=has_next,
        )


__all__: tuple[str, ...] = (
    "Pagination",
    "PaginationResult",
    "CursorPagination",
    "CursorPaginationResult",
)

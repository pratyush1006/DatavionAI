"""
Serializer field definitions for Holidays.
"""

from __future__ import annotations

from typing import Final

HOLIDAY_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "date",
    "holiday_type",
    "is_recurring_yearly",
)

HOLIDAY_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "organization_id",
    "name",
    "date",
    "holiday_type",
    "description",
    "is_recurring_yearly",
    "created_at",
    "updated_at",
)

HOLIDAY_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "name",
    "date",
    "holiday_type",
    "description",
    "is_recurring_yearly",
)

__all__ = [
    "HOLIDAY_LIST_FIELDS",
    "HOLIDAY_DETAIL_FIELDS",
    "HOLIDAY_WRITE_FIELDS",
]

"""
Serializer field definitions for the financial_report model.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "title",
    "report_type",
    "status",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "title",
    "report_type",
    "period_start",
    "period_end",
    "status",
    "generated_at",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "title",
    "report_type",
    "period_start",
    "period_end",
    "status",
    "generated_at",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "title",
    "report_type",
    "period_start",
    "period_end",
    "status",
    "generated_at",
    "is_active",
)

READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "created_at",
    "updated_at",
)

__all__ = [
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "READ_ONLY_FIELDS",
    "UPDATE_FIELDS",
    "WRITE_FIELDS",
]

"""
Serializer field definitions for the tax_filing model.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "period",
    "tax_rate",
    "status",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "tax_rate",
    "period",
    "period_start",
    "period_end",
    "reference",
    "taxable_amount",
    "tax_amount",
    "status",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "tax_rate",
    "period",
    "period_start",
    "period_end",
    "reference",
    "taxable_amount",
    "tax_amount",
    "status",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "period",
    "period_start",
    "period_end",
    "reference",
    "taxable_amount",
    "tax_amount",
    "status",
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

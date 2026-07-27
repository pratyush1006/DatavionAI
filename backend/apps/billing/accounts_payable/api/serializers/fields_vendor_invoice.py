"""
Serializer field definitions for the vendor_invoice model.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "invoice_number",
    "vendor",
    "amount",
    "due_date",
    "status",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "vendor",
    "invoice_number",
    "reference",
    "amount",
    "tax_amount",
    "due_date",
    "status",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "vendor",
    "invoice_number",
    "reference",
    "amount",
    "tax_amount",
    "due_date",
    "status",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "invoice_number",
    "reference",
    "amount",
    "tax_amount",
    "due_date",
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

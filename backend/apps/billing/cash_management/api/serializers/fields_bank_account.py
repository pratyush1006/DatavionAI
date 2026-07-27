"""
Serializer field definitions for the bank_account model.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "reference",
    "bank_account",
    "amount",
    "transaction_type",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "bank_account",
    "reference",
    "transaction_type",
    "amount",
    "description",
    "transaction_date",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "bank_account",
    "reference",
    "transaction_type",
    "amount",
    "description",
    "transaction_date",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "reference",
    "transaction_type",
    "amount",
    "description",
    "transaction_date",
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

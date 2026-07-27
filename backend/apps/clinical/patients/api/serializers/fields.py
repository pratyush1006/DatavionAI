"""
Serializer field definitions for the Patients application.
"""

from __future__ import annotations

from typing import Final

LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "mrn",
    "display_name",
    "gender",
    "phone",
    "status",
    "is_active",
)

DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "organization",
    "mrn",
    "first_name",
    "middle_name",
    "last_name",
    "preferred_name",
    "display_name",
    "age",
    "date_of_birth",
    "gender",
    "marital_status",
    "blood_group",
    "phone",
    "email",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "status",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS: Final[tuple[str, ...]] = (
    "organization",
    "mrn",
    "first_name",
    "middle_name",
    "last_name",
    "preferred_name",
    "date_of_birth",
    "gender",
    "marital_status",
    "blood_group",
    "phone",
    "email",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "status",
    "is_active",
)

UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "first_name",
    "middle_name",
    "last_name",
    "preferred_name",
    "date_of_birth",
    "gender",
    "marital_status",
    "blood_group",
    "phone",
    "email",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "status",
    "is_active",
)

READ_ONLY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "display_name",
    "age",
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

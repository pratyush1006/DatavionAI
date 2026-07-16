"""
Serializer field definitions for the Patients application.
"""

from __future__ import annotations

from typing import Final

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "mrn",
    "first_name",
    "last_name",
    "gender",
    "phone",
    "status",
    "is_active",
)

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
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
    "created_at",
    "updated_at",
)

_WRITE_FIELDS: Final[tuple[str, ...]] = (
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

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
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

__all__ = [
    "_DETAIL_FIELDS",
    "_LIST_FIELDS",
    "_UPDATE_FIELDS",
    "_WRITE_FIELDS",
]

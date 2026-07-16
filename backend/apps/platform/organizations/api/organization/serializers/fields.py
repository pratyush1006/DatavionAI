"""
Serializer field definitions for the Organizations application.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------

_SUMMARY_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "display_name",
    "code",
    "slug",
)


# ---------------------------------------------------------------------
# List
# ---------------------------------------------------------------------

_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "display_name",
    "code",
    "category",
    "organization_type",
    "status",
    "city",
    "country",
    "is_active",
)


# ---------------------------------------------------------------------
# Detail
# ---------------------------------------------------------------------

_DETAIL_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "name",
    "display_name",
    "code",
    "slug",
    "category",
    "organization_type",
    "status",
    "size",
    "email",
    "support_email",
    "phone",
    "website",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "timezone",
    "registration_number",
    "tax_number",
    "license_number",
    "accreditation",
    "verification_status",
    "subscription_status",
    "description",
    "is_verified",
    "is_demo",
    "is_active",
    "created_at",
    "updated_at",
)


# ---------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------

_WRITE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "display_name",
    "code",
    "slug",
    "category",
    "organization_type",
    "status",
    "size",
    "email",
    "support_email",
    "phone",
    "website",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "timezone",
    "registration_number",
    "tax_number",
    "license_number",
    "accreditation",
    "description",
    "is_demo",
    "is_active",
)


# ---------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------

_UPDATE_FIELDS: Final[tuple[str, ...]] = (
    "name",
    "display_name",
    "category",
    "organization_type",
    "status",
    "size",
    "email",
    "support_email",
    "phone",
    "website",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "timezone",
    "registration_number",
    "tax_number",
    "license_number",
    "accreditation",
    "description",
    "is_demo",
    "is_active",
)


__all__ = [
    "_SUMMARY_FIELDS",
    "_LIST_FIELDS",
    "_DETAIL_FIELDS",
    "_WRITE_FIELDS",
    "_UPDATE_FIELDS",
]

"""
Shared serializer field definitions for the Accounts application.
"""

from __future__ import annotations

#
# Shared field groups
#

COMMON_FIELDS = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
)

STATUS_FIELDS = (
    "is_active",
    "is_verified",
)

AUDIT_FIELDS = (
    "created_at",
    "updated_at",
)

#
# Serializer field sets
#

LIST_FIELDS = (
    *COMMON_FIELDS,
    *STATUS_FIELDS,
)

DETAIL_FIELDS = (
    *COMMON_FIELDS,
    *STATUS_FIELDS,
    *AUDIT_FIELDS,
)

CREATE_FIELDS = (
    "username",
    "email",
    "first_name",
    "last_name",
    "password",
    "is_active",
)

UPDATE_FIELDS = (
    "first_name",
    "last_name",
    "email",
    "password",
    "is_active",
)

SUMMARY_FIELDS = (
    "id",
    "username",
    "email",
    "is_active",
)


__all__ = [
    "AUDIT_FIELDS",
    "COMMON_FIELDS",
    "CREATE_FIELDS",
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "STATUS_FIELDS",
    "SUMMARY_FIELDS",
    "UPDATE_FIELDS",
]

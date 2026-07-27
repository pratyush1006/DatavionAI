"""
Shared serializer field definitions for the Accounts application.
"""

from __future__ import annotations

#
# Shared public identity fields
#

COMMON_FIELDS = (
    "id",
    "email",
    "first_name",
    "last_name",
    "phone",
)


STATUS_FIELDS = ("is_verified",)


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
    "email",
    "first_name",
    "last_name",
    "phone",
    "password",
)


UPDATE_FIELDS = (
    "first_name",
    "last_name",
    "phone",
    "email",
    "password",
)


SUMMARY_FIELDS = (
    "id",
    "email",
    "first_name",
    "last_name",
)


__all__ = (
    "AUDIT_FIELDS",
    "COMMON_FIELDS",
    "CREATE_FIELDS",
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "STATUS_FIELDS",
    "SUMMARY_FIELDS",
    "UPDATE_FIELDS",
)

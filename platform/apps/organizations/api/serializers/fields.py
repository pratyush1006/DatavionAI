"""
Serializer field definitions for the Organizations app.
"""

LIST_FIELDS = (
    "id",
    "name",
    "code",
    "organization_type",
    "city",
    "country",
    "is_active",
)

DETAIL_FIELDS = (
    "id",
    "name",
    "code",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
    "created_at",
    "updated_at",
)

WRITE_FIELDS = (
    "name",
    "code",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
)

UPDATE_FIELDS = (
    "name",
    "organization_type",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "country",
    "is_active",
)

"""
Reusable serializer fields for providers.

Defines API exposure rules for
Provider bounded context.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.providers.models import Provider

LIST_FIELDS = (
    "id",
    "provider_number",
    "employee",
    "provider_type",
    "consultation_fee",
    "status",
    "is_accepting_patients",
)


DETAIL_FIELDS = (
    *LIST_FIELDS,
    "organization",
    "years_of_experience",
    "bio",
    "display_name",
    "full_name",
    "created_at",
    "updated_at",
)


WRITE_FIELDS = (
    "employee",
    "provider_number",
    "provider_type",
    "years_of_experience",
    "consultation_fee",
    "is_accepting_patients",
    "bio",
)


UPDATE_FIELDS = (
    "provider_number",
    "provider_type",
    "years_of_experience",
    "consultation_fee",
    "is_accepting_patients",
    "bio",
)


READ_ONLY_FIELDS = (
    "id",
    "organization",
    "status",
    "display_name",
    "full_name",
    "created_at",
    "updated_at",
)


class ProviderFieldsSerializer(
    serializers.ModelSerializer,
):
    """
    Shared provider serializer fields.
    """

    display_name = serializers.ReadOnlyField()

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Provider

        fields = DETAIL_FIELDS

        read_only_fields = READ_ONLY_FIELDS


__all__ = (
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "ProviderFieldsSerializer",
    "READ_ONLY_FIELDS",
    "UPDATE_FIELDS",
    "WRITE_FIELDS",
)

"""
Reusable serializer fields for providers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.providers.models import Provider


class ProviderFieldsSerializer(serializers.ModelSerializer):
    """
    Shared provider serializer fields.
    """

    class Meta:
        model = Provider

        fields = (
            "id",
            "organization",
            "employee",
            "provider_number",
            "license_number",
            "provider_type",
            "years_of_experience",
            "is_accepting_patients",
            "bio",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

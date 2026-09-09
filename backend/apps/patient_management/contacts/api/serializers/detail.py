"""
Serializer for retrieving patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.models import Contact


class ContactDetailSerializer(serializers.ModelSerializer):
    """
    Detailed read representation of a patient contact.

    This serializer is read-only and contains no mutation behavior.
    """

    patient_id = serializers.UUIDField(
        source="patient_id",
        read_only=True,
    )

    organization_id = serializers.UUIDField(
        source="organization_id",
        read_only=True,
    )

    class Meta:
        model = Contact

        fields = (
            "id",
            "organization_id",
            "patient_id",
            "contact_type",
            "purpose",
            "value",
            "status",
            "source",
            "is_primary",
            "is_preferred",
            "created_at",
            "updated_at",
            "deleted_at",
        )

        read_only_fields = fields


__all__ = ("ContactDetailSerializer",)

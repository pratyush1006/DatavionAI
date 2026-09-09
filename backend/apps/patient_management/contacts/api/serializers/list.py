"""
Serializer for listing patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.models import Contact


class ContactListSerializer(serializers.ModelSerializer):
    """
    Lightweight read representation used by contact list endpoints.
    """

    patient_id = serializers.UUIDField(
        source="patient_id",
        read_only=True,
    )

    class Meta:
        model = Contact

        fields = (
            "id",
            "patient_id",
            "contact_type",
            "purpose",
            "value",
            "status",
            "source",
            "is_primary",
            "is_preferred",
        )

        read_only_fields = fields


__all__ = ("ContactListSerializer",)

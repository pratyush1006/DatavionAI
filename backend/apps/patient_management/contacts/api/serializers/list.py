"""
Serializer for listing patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.models import Contact


class ContactListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing patient contacts.
    """

    class Meta:
        model = Contact
        fields = (
            "id",
            "contact_type",
            "purpose",
            "value",
            "status",
            "is_primary",
            "is_preferred",
        )
        read_only_fields = fields

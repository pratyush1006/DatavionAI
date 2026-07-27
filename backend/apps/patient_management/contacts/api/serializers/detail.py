"""
Serializer for retrieving patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.models import Contact


class ContactDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a patient contact.
    """

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        )

"""
Serializer for creating patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.models import Contact


class ContactCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a patient contact.
    """

    class Meta:
        model = Contact
        exclude = (
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        )

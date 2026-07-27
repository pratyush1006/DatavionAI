"""
Serializer for updating patient contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.contacts.models import Contact


class ContactUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a patient contact.
    """

    class Meta:
        model = Contact
        exclude = (
            "id",
            "organization",
            "patient",
            "created_at",
            "updated_at",
            "deleted_at",
        )

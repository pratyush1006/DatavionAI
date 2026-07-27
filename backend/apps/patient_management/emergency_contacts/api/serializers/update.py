"""
Update serializer for Emergency Contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from ...models import EmergencyContact
from ...services import EmergencyContactService


class EmergencyContactUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Update serializer.
    """

    class Meta:
        model = EmergencyContact

        read_only_fields = (
            "uuid",
            "organization",
            "patient",
            "emergency_contact_number",
            "is_verified",
            "verified_at",
            "verified_by",
            "created_at",
            "updated_at",
        )

        fields = "__all__"

    def update(
        self,
        instance,
        validated_data,
    ):
        return EmergencyContactService.update(
            instance,
            **validated_data,
        )

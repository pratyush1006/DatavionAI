"""
Create serializer for Emergency Contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from ...models import EmergencyContact
from ...services import EmergencyContactService


class EmergencyContactCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Create serializer.
    """

    class Meta:
        model = EmergencyContact

        exclude = (
            "uuid",
            "created_at",
            "updated_at",
            "organization",
            "emergency_contact_number",
            "is_verified",
            "verified_at",
            "verified_by",
        )

    def create(
        self,
        validated_data,
    ):
        request = self.context["request"]

        return EmergencyContactService.create(
            organization=request.user.organization,
            **validated_data,
        )

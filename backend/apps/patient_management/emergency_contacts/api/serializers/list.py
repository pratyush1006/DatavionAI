"""
List serializer for Emergency Contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from ...models import EmergencyContact


class EmergencyContactListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer used for listing emergency contacts.
    """

    patient_uuid = serializers.UUIDField(
        source="patient.uuid",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    organization_uuid = serializers.UUIDField(
        source="organization.uuid",
        read_only=True,
    )

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = EmergencyContact

        fields = (
            "uuid",
            "emergency_contact_number",
            "patient_uuid",
            "patient_name",
            "organization_uuid",
            "organization_name",
            "first_name",
            "middle_name",
            "last_name",
            "relationship",
            "mobile_number",
            "preferred_contact_method",
            "is_primary",
            "priority_order",
            "status",
            "is_verified",
        )

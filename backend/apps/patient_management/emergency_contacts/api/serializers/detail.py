"""
Detail serializer for Emergency Contacts.
"""

from __future__ import annotations

from rest_framework import serializers

from ...models import EmergencyContact


class EmergencyContactDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detailed emergency contact serializer.
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

    verified_by_name = serializers.CharField(
        source="verified_by.get_full_name",
        read_only=True,
    )

    class Meta:
        model = EmergencyContact

        fields = "__all__"

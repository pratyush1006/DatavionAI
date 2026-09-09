"""Emergency contact detail serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency.models import EmergencyContact


class EmergencyDetailSerializer(serializers.ModelSerializer):
    """Serialize an emergency contact for detail responses."""

    patient_id = serializers.UUIDField(
        source="patient.id",
        read_only=True,
    )

    class Meta:
        """Define serialized emergency contact fields."""

        model = EmergencyContact
        fields = (
            "id",
            "organization",
            "patient_id",
            "name",
            "relationship",
            "phone",
            "alternate_phone",
            "email",
            "priority",
            "status",
            "notes",
            "created_at",
            "updated_at",
        )


__all__ = ("EmergencyDetailSerializer",)

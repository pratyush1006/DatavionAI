"""Emergency contact list serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency.models import EmergencyContact


class EmergencyListSerializer(serializers.ModelSerializer):
    """Serialize compact emergency contact list records."""

    class Meta:
        """Define list response fields."""

        model = EmergencyContact
        fields = (
            "id",
            "patient",
            "name",
            "relationship",
            "phone",
            "priority",
            "status",
        )


__all__ = ("EmergencyListSerializer",)

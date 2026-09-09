"""Patient Communication list serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationListSerializer(serializers.ModelSerializer):
    """Serialize Patient Communication list results."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = (
            "id",
            "patient",
            "organization",
            "channel",
            "direction",
            "communication_type",
            "status",
            "subject",
            "occurred_at",
            "created_at",
            "updated_at",
            "is_active",
        )


__all__ = ("CommunicationListSerializer",)

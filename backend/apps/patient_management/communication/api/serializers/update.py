"""Patient Communication update serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationUpdateSerializer(serializers.ModelSerializer):
    """Validate mutable Patient Communication fields."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = (
            "channel",
            "direction",
            "communication_type",
            "subject",
            "content",
            "external_reference",
            "occurred_at",
            "metadata",
        )


__all__ = ("CommunicationUpdateSerializer",)

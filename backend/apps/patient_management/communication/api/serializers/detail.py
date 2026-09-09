"""Patient Communication detail serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.communication.models import PatientCommunication


class CommunicationDetailSerializer(serializers.ModelSerializer):
    """Serialize a complete Patient Communication record."""

    class Meta:
        """Serializer metadata."""

        model = PatientCommunication
        fields = "__all__"


__all__ = ("CommunicationDetailSerializer",)

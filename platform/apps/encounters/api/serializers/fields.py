"""
Encounter serializer fields.
"""

from __future__ import annotations

from rest_framework import serializers


class PatientFieldSerializer(serializers.Serializer):
    """
    Lightweight patient serializer.
    """

    id = serializers.UUIDField()

    full_name = serializers.CharField()

    mrn = serializers.CharField()


class ProviderFieldSerializer(serializers.Serializer):
    """
    Lightweight provider serializer.
    """

    id = serializers.UUIDField()

    full_name = serializers.CharField()

    provider_number = serializers.CharField()


class AppointmentFieldSerializer(serializers.Serializer):
    """
    Lightweight appointment serializer.
    """

    id = serializers.UUIDField()

    appointment_number = serializers.CharField()

    status = serializers.CharField()


__all__ = [
    "AppointmentFieldSerializer",
    "PatientFieldSerializer",
    "ProviderFieldSerializer",
]

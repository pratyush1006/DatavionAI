"""Emergency contact update serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency.constants import (
    EmergencyContactPriority,
    EmergencyContactType,
)


class EmergencyUpdateSerializer(serializers.Serializer):
    """Validate mutable emergency contact fields."""

    name = serializers.CharField(
        max_length=255,
        required=False,
    )
    relationship = serializers.ChoiceField(
        choices=EmergencyContactType.choices,
        required=False,
    )
    phone = serializers.CharField(
        max_length=64,
        required=False,
    )
    alternate_phone = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    priority = serializers.ChoiceField(
        choices=EmergencyContactPriority.choices,
        required=False,
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )


__all__ = ("EmergencyUpdateSerializer",)

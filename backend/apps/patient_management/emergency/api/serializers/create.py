"""Emergency contact creation serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.emergency.constants import (
    EmergencyContactPriority,
    EmergencyContactType,
)


class EmergencyCreateSerializer(serializers.Serializer):
    """Validate emergency contact creation input."""

    patient_id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    relationship = serializers.ChoiceField(
        choices=EmergencyContactType.choices,
    )
    phone = serializers.CharField(max_length=64)
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
        default=EmergencyContactPriority.SECONDARY,
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )


__all__ = ("EmergencyCreateSerializer",)

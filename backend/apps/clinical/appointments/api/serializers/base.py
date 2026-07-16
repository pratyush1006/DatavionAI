"""
Base appointment serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.appointments.models import Appointment


class AppointmentBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for appointments.
    """

    class Meta:
        model = Appointment

        fields = (
            "id",
            "organization",
            "patient",
            "provider",
            "appointment_number",
            "appointment_type",
            "status",
            "priority",
            "scheduled_start",
            "scheduled_end",
            "duration_minutes",
            "reason",
            "notes",
            "check_in_at",
            "check_out_at",
            "cancellation_reason",
            "is_virtual",
            "meeting_url",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "AppointmentBaseSerializer",
]

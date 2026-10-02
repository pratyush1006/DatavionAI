"""Clinical Appointment API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.appointments.constants import (
    AppointmentPriority,
    AppointmentType,
)
from apps.clinical.appointments.models import Appointment


class AppointmentCreateSerializer(serializers.Serializer):
    """Validate appointment creation payloads."""

    appointment_number = serializers.CharField(max_length=64)
    patient_id = serializers.UUIDField()
    provider_id = serializers.UUIDField()
    appointment_type = serializers.ChoiceField(
        choices=AppointmentType.choices,
        required=False,
        default=AppointmentType.IN_PERSON,
    )
    priority = serializers.ChoiceField(
        choices=AppointmentPriority.choices,
        required=False,
        default=AppointmentPriority.ROUTINE,
    )
    scheduled_start = serializers.DateTimeField()
    scheduled_end = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField(
        required=False,
        min_value=1,
        default=30,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
    is_virtual = serializers.BooleanField(
        required=False,
        default=False,
    )
    meeting_url = serializers.URLField(
        required=False,
        allow_blank=True,
        default="",
    )


class AppointmentUpdateSerializer(serializers.Serializer):
    """Validate mutable appointment fields."""

    appointment_type = serializers.ChoiceField(
        choices=AppointmentType.choices,
        required=False,
    )
    priority = serializers.ChoiceField(
        choices=AppointmentPriority.choices,
        required=False,
    )
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    is_virtual = serializers.BooleanField(
        required=False,
    )
    meeting_url = serializers.URLField(
        required=False,
        allow_blank=True,
    )


class AppointmentRescheduleSerializer(serializers.Serializer):
    """Validate appointment rescheduling payloads."""

    scheduled_start = serializers.DateTimeField()
    scheduled_end = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField(
        required=False,
        min_value=1,
        default=30,
    )


class AppointmentCancelSerializer(serializers.Serializer):
    """Validate appointment cancellation payloads."""

    reason = serializers.CharField(
        allow_blank=False,
    )


class AppointmentDepositVerifySerializer(serializers.Serializer):
    """Validate the Razorpay callback for an appointment deposit."""

    razorpay_order_id = serializers.CharField(max_length=128)
    razorpay_payment_id = serializers.CharField(max_length=128)
    razorpay_signature = serializers.CharField(max_length=256)


class AppointmentCheckInSerializer(serializers.Serializer):
    """Validate the recording-consent choice during check-in."""

    recording_consent = serializers.BooleanField(required=True)


class AppointmentSerializer(serializers.ModelSerializer):
    """Serialize Appointment responses."""

    class Meta:
        """Define response fields."""

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
            "reschedule_count",
            "can_reschedule",
            "consultation_fee",
            "deposit_amount",
            "deposit_invoice_id",
            "final_invoice_id",
            "deposit_paid",
            "reason",
            "notes",
            "check_in_at",
            "check_out_at",
            "cancellation_reason",
            "is_virtual",
            "meeting_url",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        )
        read_only_fields = (
            "id",
            "organization",
            "status",
            "reschedule_count",
            "can_reschedule",
            "consultation_fee",
            "deposit_amount",
            "deposit_invoice_id",
            "final_invoice_id",
            "deposit_paid",
            "check_in_at",
            "check_out_at",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
            "deleted_at",
            "deleted_by_id",
        )


__all__ = (
    "AppointmentCancelSerializer",
    "AppointmentCheckInSerializer",
    "AppointmentCreateSerializer",
    "AppointmentDepositVerifySerializer",
    "AppointmentRescheduleSerializer",
    "AppointmentSerializer",
    "AppointmentUpdateSerializer",
)

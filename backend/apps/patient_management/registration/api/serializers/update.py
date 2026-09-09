"""
Update serializer for the Patient Registration module.

The serializer performs API-level validation and representation only.
Domain mutation is handled by the registration update workflow and
PatientRegistrationService.
"""

from __future__ import annotations

from apps.patient_management.registration.models import (
    PatientRegistration,
)
from rest_framework import serializers


class PatientRegistrationUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating mutable patient registration fields.

    This serializer deliberately does not override ``update()``.
    Persistence is performed by the registration update workflow.
    """

    class Meta:
        model = PatientRegistration

        fields = (
            "registration_type",
            "registration_source",
            "visit_type",
            "priority",
            "verification_method",
            "registration_datetime",
            "notes",
        )

        read_only_fields = (
            "uuid",
            "organization",
            "patient",
            "registration_number",
            "registration_status",
            "verified",
            "verified_at",
            "verified_by",
            "checked_in_at",
            "completed_at",
            "cancellation_reason",
            "cancellation_notes",
            "created_at",
            "updated_at",
        )

    def validate_notes(self, value: str | None) -> str | None:
        """
        Normalize optional registration notes.
        """
        if value is None:
            return None

        return value.strip()


__all__ = ("PatientRegistrationUpdateSerializer",)

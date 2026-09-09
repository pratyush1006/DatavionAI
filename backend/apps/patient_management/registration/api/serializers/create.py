"""
Create serializer for the Patient Registration module.

The serializer performs API-level validation and representation only.
Organization resolution, authorization, workflow orchestration, domain
validation, registration-number generation, persistence, and event
publication are handled by the workflow and domain service layers.
"""

from __future__ import annotations

from apps.patient_management.registration.models import (
    PatientRegistration,
)
from rest_framework import serializers


class PatientRegistrationCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating a patient registration.

    Organization is intentionally not accepted from the client. The active
    organization is resolved by the API/workflow context to prevent
    cross-organization registration creation.
    """

    class Meta:
        model = PatientRegistration

        fields = (
            "patient",
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


__all__ = ("PatientRegistrationCreateSerializer",)

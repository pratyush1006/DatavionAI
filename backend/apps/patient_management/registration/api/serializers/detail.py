"""
Detail serializer for the Patient Registration module.

The serializer is responsible only for API representation.
Authorization, workflow orchestration, and persistence remain outside
the serializer layer.
"""

from __future__ import annotations

from apps.patient_management.registration.models import (
    PatientRegistration,
)
from rest_framework import serializers


class PatientRegistrationDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Read-only serializer for retrieving a patient registration.
    """

    patient_uuid = serializers.UUIDField(
        source="patient.id",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    medical_record_number = serializers.CharField(
        source="patient.mrn",
        read_only=True,
    )

    organization_uuid = serializers.UUIDField(
        source="organization.id",
        read_only=True,
    )

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    verified_by_uuid = serializers.UUIDField(
        source="verified_by.id",
        read_only=True,
        allow_null=True,
    )

    verified_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PatientRegistration

        fields = (
            "id",
            "organization_uuid",
            "organization_name",
            "patient_uuid",
            "patient_name",
            "medical_record_number",
            "registration_number",
            "registration_type",
            "registration_status",
            "registration_source",
            "visit_type",
            "priority",
            "verification_method",
            "verified",
            "verified_by_uuid",
            "verified_by_name",
            "verified_at",
            "registration_datetime",
            "checked_in_at",
            "completed_at",
            "cancellation_reason",
            "cancellation_notes",
            "notes",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_verified_by_name(self, obj):
        """
        Return the verifier's human-readable name when available.
        """
        user = obj.verified_by

        if user is None:
            return None

        full_name = (f"{user.first_name} {user.last_name}").strip()

        return full_name or user.email or user.username


__all__ = ("PatientRegistrationDetailSerializer",)

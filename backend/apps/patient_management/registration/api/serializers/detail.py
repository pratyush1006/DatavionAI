"""
Detail serializer for the Patient Registration module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for retrieving a patient registration.
    """

    patient_uuid = serializers.UUIDField(
        source="patient.uuid",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    medical_record_number = serializers.CharField(
        source="patient.medical_record_number",
        read_only=True,
    )

    organization_uuid = serializers.UUIDField(
        source="organization.uuid",
        read_only=True,
    )

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    verified_by_uuid = serializers.UUIDField(
        source="verified_by.uuid",
        read_only=True,
        allow_null=True,
    )

    verified_by_name = serializers.CharField(
        source="verified_by.full_name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = PatientRegistration

        fields = (
            "uuid",
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

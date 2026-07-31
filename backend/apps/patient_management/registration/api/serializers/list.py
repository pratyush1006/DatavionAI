"""
List serializer for the Patient Registration module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing patient registrations.
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

    class Meta:
        model = PatientRegistration

        fields = (
            "uuid",
            "registration_number",
            "patient_uuid",
            "patient_name",
            "medical_record_number",
            "organization_uuid",
            "organization_name",
            "registration_type",
            "registration_status",
            "registration_source",
            "visit_type",
            "priority",
            "verified",
            "registration_datetime",
        )

        read_only_fields = fields

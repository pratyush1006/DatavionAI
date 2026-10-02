"""
List serializer for the Patient Registration module.

The serializer is responsible only for API representation.
Authorization, workflow orchestration, and persistence remain outside
the serializer layer.
"""

from __future__ import annotations

from apps.patient_management.registration.models import (
    PatientRegistration,
)
from rest_framework import serializers


class PatientRegistrationListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing patient registrations.

    Patient and organization information is exposed as read-only
    representation data. No mutation or authorization logic belongs here.
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

    class Meta:
        model = PatientRegistration

        fields = (
            "id",
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


__all__ = ("PatientRegistrationListSerializer",)

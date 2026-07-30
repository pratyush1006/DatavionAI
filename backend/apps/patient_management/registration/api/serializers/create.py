"""
Create serializer for the Patient Registration module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.registration.models import (
    PatientRegistration,
)
from apps.patient_management.registration.services import (
    PatientRegistrationService,
)


class PatientRegistrationCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating a patient registration.
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
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict,
    ) -> PatientRegistration:
        """
        Create a patient registration.
        """

        request = self.context["request"]

        return PatientRegistrationService.create_registration(
            organization=request.user.organization,
            created_by=request.user,
            **validated_data,
        )

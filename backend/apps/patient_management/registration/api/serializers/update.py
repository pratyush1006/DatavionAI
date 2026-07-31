"""
Update serializer for the Patient Registration module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.registration.models import (
    PatientRegistration,
)
from apps.patient_management.registration.services import (
    PatientRegistrationService,
)


class PatientRegistrationUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating a patient registration.
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

    def update(
        self,
        instance: PatientRegistration,
        validated_data: dict,
    ) -> PatientRegistration:
        """
        Update a patient registration.
        """

        return PatientRegistrationService.update_registration(
            registration=instance,
            **validated_data,
        )

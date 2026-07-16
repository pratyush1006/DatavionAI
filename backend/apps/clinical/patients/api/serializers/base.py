"""
Base serializers for the Patients application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.patients.models import Patient


class PatientBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared validation logic.
    """

    class Meta:
        model = Patient
        fields: tuple[str, ...] = ()

    def validate_mrn(
        self,
        value: str,
    ) -> str:
        """
        Normalize the Medical Record Number.
        """

        return value.strip().upper()

    def validate_first_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's first name.
        """

        return value.strip()

    def validate_middle_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's middle name.
        """

        return value.strip()

    def validate_last_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's last name.
        """

        return value.strip()

    def validate_preferred_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's preferred name.
        """

        return value.strip()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's email.
        """

        if not value:
            return value

        return value.strip().lower()


__all__ = [
    "PatientBaseSerializer",
]

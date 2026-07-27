"""
Base serializers for the Patients application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.patients.models import Patient


class PatientBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared normalization logic for patient serializers.
    """

    class Meta:
        model = Patient
        fields: tuple[str, ...] = ()

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        """
        Normalize a text value.
        """

        return value.strip()

    @staticmethod
    def _normalize_email(
        value: str,
    ) -> str:
        """
        Normalize an email address.
        """

        return value.strip().lower()

    def validate_mrn(
        self,
        value: str,
    ) -> str:
        """
        Normalize the Medical Record Number (MRN).
        """

        return self._normalize_text(
            value,
        ).upper()

    def validate_first_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's first name.
        """

        return self._normalize_text(
            value,
        )

    def validate_middle_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's middle name.
        """

        return self._normalize_text(
            value,
        )

    def validate_last_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's last name.
        """

        return self._normalize_text(
            value,
        )

    def validate_preferred_name(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's preferred name.
        """

        return self._normalize_text(
            value,
        )

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the patient's email address.
        """

        if not value:
            return value

        return self._normalize_email(
            value,
        )


__all__ = [
    "PatientBaseSerializer",
]

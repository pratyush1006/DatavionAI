"""
Create serializer for the Patients application.
"""

from __future__ import annotations

from .base import PatientBaseSerializer
from .fields import _WRITE_FIELDS


class PatientCreateSerializer(PatientBaseSerializer):
    """
    Serializer used for creating patients.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = _WRITE_FIELDS

    def validate_mrn(
        self,
        value: str,
    ) -> str:
        """
        Normalize the Medical Record Number.
        """

        return value.strip().upper()


__all__ = [
    "PatientCreateSerializer",
]

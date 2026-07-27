"""
Detail serializer for the Patients application.
"""

from __future__ import annotations

from .base import PatientBaseSerializer
from .fields import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class PatientDetailSerializer(PatientBaseSerializer):
    """
    Serializer used for retrieving patient details.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "PatientDetailSerializer",
]

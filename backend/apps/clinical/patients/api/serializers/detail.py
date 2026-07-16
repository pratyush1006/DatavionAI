"""
Detail serializer for the Patients application.
"""

from __future__ import annotations

from .base import PatientBaseSerializer
from .fields import _DETAIL_FIELDS


class PatientDetailSerializer(PatientBaseSerializer):
    """
    Serializer used for retrieving patient details.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = _DETAIL_FIELDS
        read_only_fields = _DETAIL_FIELDS


__all__ = [
    "PatientDetailSerializer",
]

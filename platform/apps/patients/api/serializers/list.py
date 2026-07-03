"""
List serializer for the Patients application.
"""

from __future__ import annotations

from .base import PatientBaseSerializer
from .fields import _LIST_FIELDS


class PatientListSerializer(PatientBaseSerializer):
    """
    Serializer used for listing patients.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = _LIST_FIELDS
        read_only_fields = _LIST_FIELDS


__all__ = [
    "PatientListSerializer",
]

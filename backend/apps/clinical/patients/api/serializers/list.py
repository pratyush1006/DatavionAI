"""
List serializer for the Patients application.
"""

from __future__ import annotations

from .base import PatientBaseSerializer
from .fields import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class PatientListSerializer(PatientBaseSerializer):
    """
    Serializer used for listing patients.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "PatientListSerializer",
]

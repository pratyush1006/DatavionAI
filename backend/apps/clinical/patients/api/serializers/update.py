"""
Update serializer for the Patients application.
"""

from __future__ import annotations

from .base import PatientBaseSerializer
from .fields import _UPDATE_FIELDS


class PatientUpdateSerializer(
    PatientBaseSerializer,
):
    """
    Serializer for updating patients.
    """

    class Meta(
        PatientBaseSerializer.Meta,
    ):
        fields = _UPDATE_FIELDS


__all__ = [
    "PatientUpdateSerializer",
]

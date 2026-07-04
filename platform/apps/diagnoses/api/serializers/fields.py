"""
Diagnosis serializer fields.
"""

from __future__ import annotations

from .base import DiagnosisBaseSerializer


class DiagnosisFieldsSerializer(
    DiagnosisBaseSerializer,
):
    """
    Serializer exposing diagnosis fields.
    """

    pass


__all__ = [
    "DiagnosisFieldsSerializer",
]

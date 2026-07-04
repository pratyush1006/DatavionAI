"""
Diagnosis list serializer.
"""

from __future__ import annotations

from .fields import DiagnosisFieldsSerializer


class DiagnosisListSerializer(
    DiagnosisFieldsSerializer,
):
    """
    Serializer for listing diagnoses.
    """

    pass


__all__ = [
    "DiagnosisListSerializer",
]

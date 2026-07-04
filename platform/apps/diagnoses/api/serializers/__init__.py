"""
Diagnosis serializers.
"""

from .base import DiagnosisBaseSerializer
from .create import DiagnosisCreateSerializer
from .detail import DiagnosisDetailSerializer
from .fields import DiagnosisFieldsSerializer
from .list import DiagnosisListSerializer
from .update import DiagnosisUpdateSerializer

__all__ = [
    "DiagnosisBaseSerializer",
    "DiagnosisCreateSerializer",
    "DiagnosisDetailSerializer",
    "DiagnosisFieldsSerializer",
    "DiagnosisListSerializer",
    "DiagnosisUpdateSerializer",
]

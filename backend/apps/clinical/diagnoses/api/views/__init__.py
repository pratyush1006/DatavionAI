"""
Diagnosis API views.
"""

from .list_create import DiagnosisListCreateAPIView
from .retrieve_update_destroy import (
    DiagnosisRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "DiagnosisListCreateAPIView",
    "DiagnosisRetrieveUpdateDestroyAPIView",
]

"""
Patient API view exports.
"""

from __future__ import annotations

from .bulk import (
    PatientBulkCreateAPIView,
    PatientBulkDeleteAPIView,
    PatientBulkUpdateAPIView,
)
from .list_create import PatientListCreateAPIView
from .retrieve_update_destroy import (
    PatientRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "PatientBulkCreateAPIView",
    "PatientBulkDeleteAPIView",
    "PatientBulkUpdateAPIView",
    "PatientListCreateAPIView",
    "PatientRetrieveUpdateDestroyAPIView",
]

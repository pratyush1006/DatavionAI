"""
Patient API views.
"""

from .lifecycle import (
    PatientActivateAPIView,
    PatientArchiveAPIView,
    PatientDeactivateAPIView,
    PatientRestoreAPIView,
)
from .list_create import (
    PatientListCreateAPIView,
)
from .retrieve_update_destroy import (
    PatientRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "PatientListCreateAPIView",
    "PatientRetrieveUpdateDestroyAPIView",
    "PatientActivateAPIView",
    "PatientDeactivateAPIView",
    "PatientArchiveAPIView",
    "PatientRestoreAPIView",
)

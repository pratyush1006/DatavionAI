"""
Patient Consent API view exports.
"""

from __future__ import annotations

from .lifecycle import (
    PatientConsentGrantView,
    PatientConsentRestoreView,
    PatientConsentRevokeView,
)
from .list_create import (
    PatientConsentListCreateView,
)
from .retrieve_update_destroy import (
    PatientConsentRetrieveUpdateDestroyView,
)

__all__ = (
    "PatientConsentGrantView",
    "PatientConsentListCreateView",
    "PatientConsentRetrieveUpdateDestroyView",
    "PatientConsentRestoreView",
    "PatientConsentRevokeView",
)

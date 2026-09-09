"""
Patient Identifier API view exports.
"""

from __future__ import annotations

from apps.patient_management.identifiers.api.views.lifecycle import (
    PatientIdentifierActivateAPIView,
    PatientIdentifierDeactivateAPIView,
    PatientIdentifierRevokeAPIView,
    PatientIdentifierSetPrimaryAPIView,
    PatientIdentifierVerifyAPIView,
)
from apps.patient_management.identifiers.api.views.list_create import (
    PatientIdentifierListCreateAPIView,
)
from apps.patient_management.identifiers.api.views.retrieve_update_destroy import (
    PatientIdentifierRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "PatientIdentifierActivateAPIView",
    "PatientIdentifierDeactivateAPIView",
    "PatientIdentifierListCreateAPIView",
    "PatientIdentifierRetrieveUpdateDestroyAPIView",
    "PatientIdentifierRevokeAPIView",
    "PatientIdentifierSetPrimaryAPIView",
    "PatientIdentifierVerifyAPIView",
)

"""
Patient Core model exports.
"""

from __future__ import annotations

from apps.patient_management.patients.models.patient import Patient
from apps.patient_management.patients.models.patient_audit_log import (
    PatientAuditAction,
    PatientAuditLog,
)

__all__ = [
    "Patient",
    "PatientAuditAction",
    "PatientAuditLog",
]

# Canonical public module identity for the Patient aggregate.
Patient.__module__ = "apps.patient_management.patients.models"

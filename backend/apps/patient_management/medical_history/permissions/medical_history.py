"""
Permission classes for the Medical History module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PatientMedicalHistoryPermission:
    VIEW = "medical_history.view"
    CREATE = "medical_history.create"
    UPDATE = "medical_history.update"
    DELETE = "medical_history.delete"


class CanViewPatientMedicalHistory(BasePermission):
    permission_code = PatientMedicalHistoryPermission.VIEW


class CanCreatePatientMedicalHistory(BasePermission):
    permission_code = PatientMedicalHistoryPermission.CREATE


class CanUpdatePatientMedicalHistory(BasePermission):
    permission_code = PatientMedicalHistoryPermission.UPDATE


class CanDeletePatientMedicalHistory(BasePermission):
    permission_code = PatientMedicalHistoryPermission.DELETE


__all__ = [
    "CanCreatePatientMedicalHistory",
    "CanDeletePatientMedicalHistory",
    "CanUpdatePatientMedicalHistory",
    "CanViewPatientMedicalHistory",
    "PatientMedicalHistoryPermission",
]

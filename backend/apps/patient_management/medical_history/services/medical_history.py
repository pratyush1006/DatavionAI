"""
Medical History services.
"""

from __future__ import annotations

from apps.patient_management.components import PatientMgmtService
from apps.patient_management.medical_history.models import PatientMedicalHistory

create_medical_history = None
update_medical_history = None
delete_medical_history = None


class PatientMedicalHistoryService(PatientMgmtService):
    """
    Write-side operations for medical history records.
    """

    model = PatientMedicalHistory


create_medical_history = PatientMedicalHistoryService.create
update_medical_history = PatientMedicalHistoryService.update
delete_medical_history = PatientMedicalHistoryService.delete


__all__ = [
    "PatientMedicalHistoryService",
    "create_medical_history",
    "delete_medical_history",
    "update_medical_history",
]

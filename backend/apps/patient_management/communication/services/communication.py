"""
Communication services.
"""

from __future__ import annotations

from apps.patient_management.communication.models import PatientCommunication
from apps.patient_management.components import PatientMgmtService

create_communication = None
update_communication = None
delete_communication = None


class PatientCommunicationService(PatientMgmtService):
    """
    Write-side operations for communication records.
    """

    model = PatientCommunication


create_communication = PatientCommunicationService.create
update_communication = PatientCommunicationService.update
delete_communication = PatientCommunicationService.delete


__all__ = [
    "PatientCommunicationService",
    "create_communication",
    "delete_communication",
    "update_communication",
]

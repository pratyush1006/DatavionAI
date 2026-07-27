"""
Patient Profile services.
"""

from __future__ import annotations

from apps.patient_management.components import PatientMgmtService
from apps.patient_management.profile.models import PatientProfile

create_profile = None
update_profile = None
delete_profile = None


class ProfileService(PatientMgmtService):
    """
    Write-side operations for patient profiles.
    """

    model = PatientProfile


create_profile = ProfileService.create
update_profile = ProfileService.update
delete_profile = ProfileService.delete


__all__ = [
    "ProfileService",
    "create_profile",
    "delete_profile",
    "update_profile",
]

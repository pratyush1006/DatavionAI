"""
Portal Account services.
"""

from __future__ import annotations

from apps.patient_management.components import PatientMgmtService
from apps.patient_management.portal.models import PatientPortalAccount

create_portal_account = None
update_portal_account = None
delete_portal_account = None


class PatientPortalAccountService(PatientMgmtService):
    """
    Write-side operations for portal account records.
    """

    model = PatientPortalAccount


create_portal_account = PatientPortalAccountService.create
update_portal_account = PatientPortalAccountService.update
delete_portal_account = PatientPortalAccountService.delete


__all__ = [
    "PatientPortalAccountService",
    "create_portal_account",
    "delete_portal_account",
    "update_portal_account",
]

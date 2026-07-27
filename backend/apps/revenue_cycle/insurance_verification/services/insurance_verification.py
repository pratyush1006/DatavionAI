"""
Insurance Verification services.
"""

from __future__ import annotations

from apps.revenue_cycle.components import RcmService
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification

create_verification = None
update_verification = None
delete_verification = None


class InsuranceVerificationService(RcmService):
    """
    Write-side operations for insurance verification records.
    """

    model = InsuranceVerification


create_verification = InsuranceVerificationService.create
update_verification = InsuranceVerificationService.update
delete_verification = InsuranceVerificationService.delete


__all__ = [
    "InsuranceVerificationService",
    "create_verification",
    "delete_verification",
    "update_verification",
]
